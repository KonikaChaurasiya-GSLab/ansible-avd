from __future__ import absolute_import, division, print_function

__metaclass__ = type


import glob

from ansible.errors import AnsibleActionFail
from ansible.plugins.action import ActionBase

import ansible_collections.arista.avd.plugins.plugin_utils.topology_generator_utils as gt


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = {}
        result = super().run(tmp, task_vars)
        del tmp  # tmp no longer has any effect
        if self._task.args and "structured_config" not in self._task.args:
            raise AnsibleActionFail("Missing 'structured_config' variable.")
        path = self._task.args["structured_config"]
        self.driver_func(path)
        return result

    def driver_func(self, directory_path):
        files = glob.glob(directory_path + "/*.yml")

        output_list = []
        for file in files:
            data = gt.read_yaml_file(file)
            node_dict = gt.create_node_dict(data, file)
            output_list = gt.structured_config_to_topology_input(output_list, node_dict, data["diagram_groups"], current_dict={})
        root_dict = gt.find_root_nodes(output_list[0])
        output_list[0]["nodes"].append(root_dict)
        global_node_list, graph_dict = gt.create_graph_dict(output_list)

        level_dict, node_level_dict = gt.find_node_levels(graph_dict, "0", global_node_list)

        # node_port_val = {top, bottom, left, right}
        node_port_val = {}

        # print(graph_dict)
        # print("========")
        # top and bottom port values
        # print("node_level_dict")
        # example 'FIREWALL': 1, 'SPINE1': 2, 'SPINE2': 2, 'LEAF1': 3
        print(node_level_dict)

        for i in node_level_dict.keys():
            node_port_val[i] = {}
            node_port_val[i]["checked"] = []
            node_port_val[i]["top"] = []
            node_port_val[i]["bottom"] = []
            node_port_val[i]["left"] = []
            node_port_val[i]["right"] = []
        print(node_port_val)

        # avoid same node neighbour pair
        check_same_node = []
        temp_graph_dict = {}

        for node_val, node_details in graph_dict.items():
            for i in node_details:
                node_neighbor_str = None

                node_neighbor_str = [node_val] + [i["nodePort"]] + [i["neighborDevice"]] + [i["neighborPort"]]
                # print(node_neighbor_str)
                # print("===")
                node_neighbor_str.sort()
                node_neighbor_str = "_".join(node_neighbor_str)
                # print(node_neighbor_str)
                if node_neighbor_str not in check_same_node:
                    check_same_node.append(node_neighbor_str)
                    if node_val not in temp_graph_dict.keys():
                        temp_graph_dict[node_val] = [i]
                    else:
                        temp_graph_dict[node_val] = temp_graph_dict[node_val] + [i]
                #'SPINE1': [{'nodePort': '1', 'neighborDevice': 'LEAF1', 'neighborPort': '1'}]
                #'FIREWALL': 1, 'SPINE1': 2, 'SPINE2': 2, 'LEAF1': 3
                # set top and bottom port values
                if node_level_dict[node_val] < node_level_dict[i["neighborDevice"]]:
                    if i["nodePort"] not in node_port_val[node_val]["bottom"] and i["nodePort"]:
                        node_port_val[node_val]["bottom"] = node_port_val[node_val]["bottom"] + [i["nodePort"]]
                        node_port_val[node_val]["checked"] = node_port_val[node_val]["checked"] + [i["nodePort"]]

                    if i["neighborPort"] not in node_port_val[i["neighborDevice"]]["top"] and i["neighborPort"]:
                        node_port_val[i["neighborDevice"]]["top"] = node_port_val[i["neighborDevice"]]["top"] + [i["neighborPort"]]
                        node_port_val[i["neighborDevice"]]["checked"] = node_port_val[i["neighborDevice"]]["checked"] + [i["neighborPort"]]

                if node_level_dict[node_val] > node_level_dict[i["neighborDevice"]]:
                    if i["nodePort"] not in node_port_val[node_val]["top"] and i["nodePort"]:
                        node_port_val[node_val]["top"] = node_port_val[node_val]["top"] + [i["nodePort"]]
                        node_port_val[node_val]["checked"] = node_port_val[node_val]["checked"] + [i["nodePort"]]

                    if i["neighborPort"] not in node_port_val[i["neighborDevice"]]["bottom"] and i["neighborPort"]:
                        node_port_val[i["neighborDevice"]]["bottom"] = node_port_val[i["neighborDevice"]]["bottom"] + [i["neighborPort"]]
                        node_port_val[i["neighborDevice"]]["checked"] = node_port_val[i["neighborDevice"]]["checked"] + [i["neighborPort"]]

        # left right ports
        # print("level_dict")
        # #example 1: ['FIREWALL'], 2: ['SPINE1', 'SPINE2'], 3: ['LEAF1', 'LEAF2', 'LEAF3', 'LEAF4'],
        # print(level_dict)
        print(node_port_val)        

        for level_list in level_dict.values():
            for i in range(len(level_list)):
                if i % 2 != 0:
                    for node_detail in graph_dict[level_list[i]]:
                        if node_detail["neighborDevice"] in level_list:
                            if (node_detail["nodePort"] not in node_port_val[level_list[i]]["left"]) and (
                                node_detail["nodePort"] not in node_port_val[level_list[i]]["checked"]
                            ):
                                node_port_val[level_list[i]]["left"] = node_port_val[level_list[i]]["left"] + [node_detail["nodePort"]]
                                node_port_val[level_list[i]]["checked"] = node_port_val[level_list[i]]["checked"] + [node_detail["nodePort"]]
                else:
                    for node_detail in graph_dict[level_list[i]]:
                        if node_detail["neighborDevice"] in level_list:
                            if (node_detail["nodePort"] not in node_port_val[level_list[i]]["right"]) and (
                                node_detail["nodePort"] not in node_port_val[level_list[i]]["checked"]
                            ):
                                node_port_val[level_list[i]]["right"] = node_port_val[level_list[i]]["right"] + [node_detail["nodePort"]]
                                node_port_val[level_list[i]]["checked"] = node_port_val[level_list[i]]["checked"] + [node_detail["nodePort"]]

        graph_dict = temp_graph_dict

        print(temp_graph_dict)

        rank_nodes_list = []
        for v in level_dict.values():
            rank_nodes_list += v
        undefined_rank_nodes = list(set(rank_nodes_list) ^ set(global_node_list))
        gt.generate_topology(level_dict, graph_dict, output_list, undefined_rank_nodes, node_port_val)
