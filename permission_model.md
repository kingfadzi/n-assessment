# Permission model 


![](entities.drawio.png)

### Nolio Instances Overview

| **Instance** | **Purpose** | **Notes** |
| --- | --- | --- |
| Sandpit | Teams to get familiar with Nolio | Not for actual deployments, refreshed monthly |
| UAT | Deployment environment | Used for testing before production |
| Production PDN | Deployment environment | Used for Dev, UAT, Prod, DR deployments |

### Access to Nolio Release Operations Center (ROC)

| **Functional Group** | **Users** | **Permissions** |
| --- | --- | --- |
| FGLBNL Dev | BTB | Manage flows, assign agents, deploy to non-production environments |
| FGLBNL Ops | RTB | Manage flows, assign agents, deploy to production environments |

### Correlation ID Usage

| **ID Type** | **Prefix for Functional Groups** |
| --- | --- |
| Architecture Model Correlation ID | FGLBNAL or FLDN |
| Business Application Correlation ID | FGLBNL or FLDN |

### Functional Group Naming Conventions

| **Environment** | **Naming Convention Example** |
| --- | --- |
| Non-Production | FGLBNL Dev APMxxxxxxx |
| Production | FGLBNL Ops APMxxxxxxx |

### Requesting New Nolio Applications

| **Request Type** | **Required Information** | **Notes** |
| --- | --- | --- |
| New Functional Groups | Functional Group Names, Business Application Correlation ID | Follow naming convention |
| New Nolio Application | Environment Names, Functional Group Names, Business Application Correlation ID | Raise incident support ticket |

### Managing Permissions

| **Environment** | **Permissions** |
| --- | --- |
| Sandpit | Superuser for all users, 30-minute automatic updates |
| Production | Permission to assign agents is based on AD functional groups and CI data from ServiceFirst |

### System Account Permissions

| **Environment** | **Group** | **Permissions** |
| --- | --- | --- |
| Non-Production | FGLBNL Dev APMxxxxxxx | Can be used in CI tools for non-prod environments |
| Production | FGLBNL Ops APMxxxxxxx | **Not permitted** to avoid risk and control breaches |
