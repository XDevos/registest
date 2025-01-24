## Usage n°1: Transformation

```bash
regis_transform -I path/to/img.tif -X 1.2 -Y 53 -Z 0.1 -O path/to/out/img.tif
```

```bash
registest -C transform --folder path/to/folder/with/data/
```

Method used by default: scipy

Filling value used : 0.0

### Parameter file

multiple:

```json
{
    "transform": [
        {"xyz": [0.5,0,0]},
        {"xyz": [0,17.1,15.0]},
        {"xyz": [-25,-10,-3]}
    ],
    "register": {},
    "compare": {}
}
```

Simple:

```json
{
    "transform": [
        {"xyz": [1.2,53,0.1]}
    ],
    "register": [],
    "compare": []
}
```



## Usage n°2: Registration

```bash
regis_register -M <method_name> -R path/to/ref.tif -T path/to/target.tif -F out/folder/
```

```bash
registest -C register --folder path/to/folder/with/data/
```

Simple:

```json
{
    "transform": [],
    "register": [
        {"method": "scipy"}
    ],
    "compare": {}
}
```



## Usage n°3: Comparison

```bash
regis_compare -R path/to/ref.tif -T path/to/target.tif -F out/folder/
```

```bash
registest -C compare --folder path/to/folder/with/data/
```

Simple:

```json
{
    "transform": [],
    "register": [],
    "compare": [
        {}
    ]
}
```

## Usage n°4: Registration + Comparison

```bash
registest -C register,compare --folder path/to/folder/with/data/
```

Simple:

```json
{
    "transform": [],
    "register": [
        {"method": "scipy"}
    ],
    "compare": []
}
```
