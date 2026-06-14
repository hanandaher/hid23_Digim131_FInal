# hid23_Digim131_FInal
## Beach Generator

### What it does:
A maya tool that generates a basic beach scene, including sand, water, palm trees, and seashells. Artists can control palm tree height, seashell variation, and size.


### Planned Features
- [x] Core geometry functions (Week 6)
- [ ] Data-driven configuration (Week 7)
- [ ] Error handling + debug mode (Week 8)
- [ ] Maya UI window + JSON save/load (Week 9)
- [ ] Polish + documentation (Week 10)



### Project Structure:
```
beach_demo/
     main.py               # Entry point, config, build_beach()
     beach_materials.py    # create_material, assign_material
     beach_geometry.py           # create_water, create_sand, create_palmtree, create_seashells
     README.md             # This File
```


### Functions

## Geometry
create_water(width, length, position) - ocean water

create_seashells(width, length, scale, positon, axis) - seashell placement

create_palmtree(width, length, scale, position, axis) - palmtree placement

create_sand(width, length, position) - sand


### Beach_materials.py
create_material(name,color) - lambert shader with RGB

assign_material(obj_name, shader_name) - Apply shader to object

### How to run:
1. Open Maya
2. Open Script Editor (Windows > General Editors > Script Editor)
3. Source main.py from the beach_demo folder

### Reflection:
This project was very fun but honestly so challenging. I find it hard to realize where small mistakes are, commas, indents, etc. I feel as though I have a somewhat good understanding of the language, I can remember what phrases do what. My biggest problem is realizing the small errors and being able to trouble shoot, I think that is the challenge.

  ## Demo Video\
(https://drexel0-my.sharepoint.com/:f:/r/personal/hid23_drexel_edu/Documents/Digim131FINALRecording?csf=1&web=1&e=2OBcFq) 

Author:
Hanan Daher | DIGIM 131 | Drexel University
