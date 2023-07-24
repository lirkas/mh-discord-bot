# Hitzone Data File Structure Info

Files containing infos such as a monster parts, hitzones resistances, stagger values, and other
combat related informations.
<br>

# Content

```js
╔══════════════╦════════╦══════════╦══════════════════════════════════════╗
║ KEY_NAME     ║ TYPE   ║ REQUIRED ║ INFOS                                ║
╠══════════════╬════════╬══════════╬══════════════════════════════════════╣
║ "name"       ║ string ║ yes      ║ monster name                         ║
╠══════════════╬════════╬══════════╬══════════════════════════════════════╣
║ "game"       ║ string ║ yes      ║ game name                            ║
╠══════════════╬════════╬══════════╬══════════════════════════════════════╣
║ "hitzone"    ║ object ║ yes      ║ contain all monsters parts           ║
╠══════════════╬════════╬══════════╬══════════════════════════════════════╣
║ "normal"     ║ array  ║ yes      ║ contains hitzone values (normal mode)║
╠══════════════╬════════╬══════════╬══════════════════════════════════════╣
║ "rage"       ║ array  ║ no       ║ contains hitzone values (rage mode)  ║
╠══════════════╬════════╬══════════╬══════════════════════════════════════╣
║ "stagger"    ║ number ║ yes      ║ stagger threshold (0 == no stagger)  ║
╠══════════════╬════════╬══════════╬══════════════════════════════════════╣
║ "notes"      ║ string ║ no       ║ text details                         ║
╠══════════════╬════════╬══════════╬══════════════════════════════════════╣
║ "notes_rage" ║ string ║ no       ║ text details (rage mode only)        ║
╠══════════════╬════════╬══════════╬══════════════════════════════════════╣
║ "rage_m"     ║ number ║ no       ║ rage mode defense multiplier value   ║
╚══════════════╩════════╩══════════╩══════════════════════════════════════╝
```

# File structure

Basic Json<br>
The code below does not contain any useful data but is valid.

Here is an more relevant [Example file](example_akantor.stats.json).
```json
{
	"name": "MONSTER_NAME",
	"game": "GAME_NAME",
	"hitzone": {
		"part_name_0": {
			"normal": [0, 0, 0, 0, 0, 0, 0, 0],
			"rage": [0, 0, 0, 0, 0, 0, 0, 0],
			"stagger": 1000
		},
		"part_name_1": {
			"normal": [0, 0, 0, 0, 0, 0, 0, 0],
			"rage": [0, 0, 0, 0, 0, 0, 0, 0],
			"stagger": 1000
		}
	},
	"rage_m": 1.0,
	"notes": "Important Things"
}
```
# Filenames

File names start with the monster name and end with `.stats.json`<br>
If another type of file already exists for this monster, both files should start with
the same name, like in the example below<br>


Existing file that contain monster drops:<br>
>`plum_daimyo_hermitaur.txt`

New file that will contain monster hitzone data:<br>
>`plum_daimyo_hermitaur.stats.json`

Folder structure for hitzone files is the same as existing ones.

Check the [monster drop files](../../files/) for names and folder structure.


# Hitzone values

Hitzone values, for a monster head part, for all weapon types and elements, in normal mode:

```json
...
"hitzone": {
	"Head": {
		"normal": [50, 60, 40, 0, 5, 20, 40, 0],
...
```

Values goes in the following order:

> `"normal": [cutting, impact, shot, fire, water, thunder, dragon, ice]`

If a value is unknown, set it to `"???"`
```json
"normal": [50, "???", 40, 0, 5, 20, 40, "???"]
```

In that case, both `impact` and `ice` values are set to unknown

**There must always be the same number of values in each hitzone array**
<br>

# Stagger values

Represents how much damage this part can receive before an animation occurs.
```json
...
"hitzone": {
	"Head": {
		"normal": [50, 60, 40, 0, 5, 20, 40, 0],
		"stagger": 600
	},
...
```

Setting the value to 0 means the part is not 'staggerable'
```json
"stagger": 0
```

# Monster 'modes'<br>

Each monster must have at least one mode for each hitzone/part ("normal" is the default one)
Each part must contain the same amount of modes as others, with matching mode names
<br>
"rage" is optional, but modes can be renamed/added if the monster has 
different, or more of them.

As an example, if a monster would have theses 4 different modes/phases:

> normal, rage, shielded, burning

and each has different hitzone values, they can be represented like this:

```json
...
"hitzone": {
	"Head": {
		"normal": [50, 60, 40, 0, 5, 20, 40, 0],
		"rage": [60, 60, 30, 0, 20, 20, 20, 0],
		"shielded": [5, 10, 5, 0, 10, 10, 10, 0],
		"burning": [80, 20, 30, 0, 20, 20, 20, 0],
		"stagger": 9000
	},
	"Neck": {
		"normal": [35, 50, 25, 0, 5, 15, 20, 0],
		"rage": [40, 50, 25, 0, 15, 15, 10, 0],
		"shielded": [10, 5, 5, 0, 5, 10, 5, 0],
		"burning": [30, 20, 10, 0, 0, 0, 5, 0],
		"stagger": 2400
	},
},
...
```

# Monster Parts

A monster with 3 different parts (Head, Neck, Back) looks like this:
```json
...
"hitzone": {
	"Head": {
		"normal": [50, 60, 40, 0, 5, 20, 40, 0],
		"stagger": 600
	},
	"Neck": {
		"normal": [35, 50, 25, 0, 5, 15, 20, 0],
		"stagger": 240
	},
	"Back": {
		"normal": [20, 25, 25, 10, 5, 15, 20, 0],
		"stagger" : 240
	}
},
...
```
There must be between 1 and any number of part.

**Part names should ideally have a maximum lenght of 10 characters.**

# Notes

```json
"notes": "Important Things",
"notes_normal": "Important Things for normal mode only",
"notes_rage": "Important Things for rage mode only"
```

That is simply plain text to be displayed with the data.<br>
It can, part break conditions, increased resistances during specific moves,
anything about the hitzones, the monster, etc.<br>

`"notes"` concerns the monster in general, regardless of his mode.<br>
`"notes_mode_a"` is specific to `mode_a`.<br>

Notes can be added for each mode the monster has, and the `mode_x` in `"notes_mode_x"`
should match the one used for hitzone values, as seen in the example below.

```json
...
"hitzone": {
	"Head": {
		"normal": [50, 60, 40, 0, 5, 20, 40, 0],
		"very_hungry": [80, 70, 50, 10, 5, 10, 30, 0],
		"stagger": 600
	}
},
"notes_normal": "",
"notes_very_hungry": "Will eat raw meat"
...
```

**Max length for each note should ideally be 200 characters.**
