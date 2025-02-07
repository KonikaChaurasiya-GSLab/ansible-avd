---
search:
  boost: 2
---

# DHCP Relay

## DHCP Relay

=== "Table"

    | Variable | Type | Required | Default | Value Restrictions | Description |
    | -------- | ---- | -------- | ------- | ------------------ | ----------- |
    | [<samp>dhcp_relay</samp>](## "dhcp_relay") | Dictionary |  |  |  |  |
    | [<samp>&nbsp;&nbsp;servers</samp>](## "dhcp_relay.servers") | List, items: String |  |  |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;- &lt;str&gt;</samp>](## "dhcp_relay.servers.[].&lt;str&gt;") | String |  |  |  | Server IP or Hostname |
    | [<samp>&nbsp;&nbsp;tunnel_requests_disabled</samp>](## "dhcp_relay.tunnel_requests_disabled") | Boolean |  |  |  |  |

=== "YAML"

    ```yaml
    dhcp_relay:
      servers:
        - <str>
      tunnel_requests_disabled: <bool>
    ```
