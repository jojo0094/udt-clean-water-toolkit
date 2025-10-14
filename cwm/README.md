# cleanwater module

## Understanding Data Structures

**New to this codebase?** Having difficulty understanding data flow and object types?

👉 **Start here**: [cleanwater/DATA_FLOW.md](cleanwater/DATA_FLOW.md)

This guide explains:
- What are nodes and edges?
- What attributes do they have?
- How are lists organized?
- Complete examples with diagrams

**Additional Resources:**
- [cleanwater/core/schemas.py](cleanwater/core/schemas.py) - Complete type definitions
- [cleanwater/core/README.md](cleanwater/core/README.md) - Quick reference
- [cleanwater/transform/README.md](cleanwater/transform/README.md) - Module guide

## 1. Requirements

### 1.1 Packages

- geopandas
- numpy
- momepy
- matplotlib
- networkx

These packages can be installed with the instructions in Section 2.


## 2. Development

TODO: add independent development.

For the time being It's easiest to develop this module when integrated in another application. 

First you will need to build a wheel of the module:

```
python3 -m pip install build

python3 -m build --wheel
```

Then see [app development](../cwa/cwa_geodjango/README.md#2-development) for how to run the module.


## 3. Tests
