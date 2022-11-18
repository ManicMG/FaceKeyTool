# FaceKeyTool
THIS ADDON IS AN EARLY VERSION - I recomend creating a new save or backup before use.
An addon for Blender to aid in working with IOS ARKit and Shapekeys in general

Most of these tools are quality of life improvements:

Add Face Keys:
-Adds the standard 52 IOS ARKit shape keys to the select mesh - These are only empty keys in order for you to edit as you wish

Apply All Modifiers:
-This is incredibly useful if you intend to use Modifiers with a model that uses ShapeKeys. Currently Blender will actually not allow you to apply your modifiers if you have ShapeKeys
-Additionally Blender will also clear ALL shapekey data upon export if a modifier is present. 
-This Tool will Duplicate your current mesh for every shapekey, set that shape key, apply and then transfer if back onto another duplicate.
-The result is a new model that is "baked" down with all modifiers applied and all shapekeys still present and working while retaining your "Working Model"

Add Suffixes to Names:
-When using Apply All Modifiers you may find you want to add a suffix to keep track of which model is you "Working" model and you "Applied Model". This does that
-You should not have to rename each time if you have this on, it should detect if your Working Suffix is already present when applying.


Create Mirror Key:
-This is just a the mirror key function but with a few quality of life improvements:
	-A duplicate key will be created instead of affecting the current key
	-It will detect if the key contains "_L", "_R", "Right", "Left" And will automatically fix the name to meet this standard
	-It will automcatically move the key up to the location of the selected key (normally they will always spawn at the bottom)
-Use Topology bool is the same function but with the Use Topology option - Honeslty Ive never really known what this does but sometimes it helps if the mirror fails.

Transfer All ShapeKeys:
	-Is just the Transfer ShapeKeys function, possible quality of life improvements to come.

Clear ShapeKey on Selected Verts:
	- Is just the "Blend from Shape" function but will blend with "Basis" and "Add" turned off. This essentially clears the ShapeKey data but ONLY on the selected verts
