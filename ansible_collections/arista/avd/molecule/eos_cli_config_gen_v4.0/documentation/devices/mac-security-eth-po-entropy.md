# mac-security-eth-po-entropy

## Table of Contents

- [Management](#management)
  - [Management Interfaces](#management-interfaces)
- [Management Security](#management-security)
  - [Management Security Summary](#management-security-summary)
  - [Management Security SSL Profiles](#management-security-ssl-profiles)
  - [Management Security Configuration](#management-security-configuration)
- [Interfaces](#interfaces)
  - [Ethernet Interfaces](#ethernet-interfaces)
  - [Port-Channel Interfaces](#port-channel-interfaces)
- [MACsec](#macsec)
  - [MACsec Summary](#macsec-summary)
  - [MACsec Device Configuration](#macsec-device-configuration)

## Management

### Management Interfaces

#### Management Interfaces Summary

##### IPv4

| Management Interface | description | Type | VRF | IP Address | Gateway |
| -------------------- | ----------- | ---- | --- | ---------- | ------- |
| Management1 | oob_management | oob | MGMT | 10.73.255.122/24 | 10.73.255.2 |

##### IPv6

| Management Interface | description | Type | VRF | IPv6 Address | IPv6 Gateway |
| -------------------- | ----------- | ---- | --- | ------------ | ------------ |
| Management1 | oob_management | oob | MGMT | - | - |

#### Management Interfaces Device Configuration

```eos
!
interface Management1
   description oob_management
   vrf MGMT
   ip address 10.73.255.122/24
```

## Management Security

### Management Security Summary

| Settings | Value |
| -------- | ----- |
| Entropy source | hardware |
| Common password encryption key | True |

### Management Security SSL Profiles

| SSL Profile Name | TLS protocol accepted | Certificate filename | Key filename | Cipher List |
| ---------------- | --------------------- | -------------------- | ------------ | ----------- |
| SSL_PROFILE | 1.1 1.2 | SSL_CERT | SSL_KEY | - |

### Management Security Configuration

```eos
!
management security
   entropy source hardware
   password encryption-key common
   ssl profile SSL_PROFILE
      tls versions 1.1 1.2
      certificate SSL_CERT key SSL_KEY
```

## Interfaces

### Ethernet Interfaces

#### Ethernet Interfaces Summary

##### L2

| Interface | Description | Mode | VLANs | Native VLAN | Trunk Group | Channel-Group |
| --------- | ----------- | ---- | ----- | ----------- | ----------- | ------------- |
| Ethernet3 | DC1-AGG01_Ethernet1 | *trunk | *1-5 | *- | *- | 3 |

*Inherited from Port-Channel Interface

##### IPv4

| Interface | Description | Type | Channel Group | IP Address | VRF |  MTU | Shutdown | ACL In | ACL Out |
| --------- | ----------- | -----| ------------- | ---------- | ----| ---- | -------- | ------ | ------- |
| Ethernet1 | - | routed | - | 1.1.1.1/24 | default | - | - | - | - |

#### Ethernet Interfaces Device Configuration

```eos
!
interface Ethernet1
   mac security profile A1
   no switchport
   ip address 1.1.1.1/24
!
interface Ethernet3
   description DC1-AGG01_Ethernet1
   mac security profile A1
   channel-group 3 mode active
```

### Port-Channel Interfaces

#### Port-Channel Interfaces Summary

##### L2

| Interface | Description | Type | Mode | VLANs | Native VLAN | Trunk Group | LACP Fallback Timeout | LACP Fallback Mode | MLAG ID | EVPN ESI |
| --------- | ----------- | ---- | ---- | ----- | ----------- | ------------| --------------------- | ------------------ | ------- | -------- |
| Port-Channel3 | L2-PORT | switched | trunk | 1-5 | - | - | - | - | - | - |

#### Port-Channel Interfaces Device Configuration

```eos
!
interface Port-Channel3
   description L2-PORT
   switchport
   switchport trunk allowed vlan 1-5
   switchport mode trunk
```

## MACsec

### MACsec Summary

License is installed.

FIPS restrictions enabled.

#### MACsec Profiles Summary

**Profile A1:**

Settings:

| Cipher | Key-Server Priority | Rekey-Period | SCI |
| ------ | ------------------- | ------------ | --- |
| aes128-gcm | - | 30 | True |

Keys:

| Key ID | Encrypted (Type 7) Key | Fallback |
| ------ | ---------------------- | -------- |
| 1234a | 025756085F535976 | - |
| 1234c | 10195F4C5144405A | True |

L2 Protocols:

| L2 Protocol | Mode |
| ----------- | ---- |
| lldp | bypass |

**Profile A2:**

Settings:

| Cipher | Key-Server Priority | Rekey-Period | SCI |
| ------ | ------------------- | ------------ | --- |
| - | - | - | - |

Keys:

| Key ID | Encrypted (Type 7) Key | Fallback |
| ------ | ---------------------- | -------- |
| 1234b | 12485744465E5A53 | - |

### MACsec Device Configuration

```eos
!
mac security
   license license1 123456
   fips restrictions
   !
   profile A1
      cipher aes128-gcm
      key 1234a 7 025756085F535976
      key 1234c 7 10195F4C5144405A fallback
      mka session rekey-period 30
      sci
      l2-protocol lldp bypass
   profile A2
      key 1234b 7 12485744465E5A53
```
