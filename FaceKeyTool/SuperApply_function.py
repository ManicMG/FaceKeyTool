import bpy
def reset_shape_keys ():	
	for name, shape_key in get_active_block().items():
		shape_key.value = 0

def get_active_block ():
	bpy.context.object.active_shape_key_index = 0
	block_id = bpy.context.object.active_shape_key.id_data.name
	return bpy.data.shape_keys[block_id].key_blocks

def select (selection):
	bpy.ops.object.select_all(action='DESELECT')
	selection.select_set(True)
	bpy.context.view_layer.objects.active = selection

def select_last_shape_key ():
	shape_key_count = len(get_active_block().items())
	bpy.context.object.active_shape_key_index = shape_key_count - 1

def remove_shape_keys (object):
	selection = bpy.context.object
	object.shape_key_clear()
	select(selection)

def apply_modifiers (object):
	selection = bpy.context.object
	select(object)

	for key, modifier in object.modifiers.items():
		if key != 'Armature':
			bpy.ops.object.modifier_apply(modifier=key)

	select(selection)		 

def super_apply_modifiers (workingSuffix, appliedSuffix, setSuffixes):
	selectedObj = bpy.context.selected_objects
	for obj in selectedObj:
		obj.select_set(False)
	for obj in selectedObj:
		select(obj)
		original = obj
		if setSuffixes == True:
			if appliedSuffix in obj.name:
				originalname = obj.name.replace(appliedSuffix, '')
			elif workingSuffix in obj.name:
				originalname = obj.name.replace(workingSuffix, '')
			else:
				originalname = obj.name
			obj.name = originalname + appliedSuffix
		else:
			originalname = obj.name
		
		#oldobj = bpy.context.scene.objects.get(originalname + appliedSuffix)
		#if oldobj:
		#	print ("DELETING OBJECT")
		#	select(oldobj)
		#	bpy.ops.object.delete(use_global=False)
			
		#select(obj)
		if "Armature" in original.modifiers:
			original.modifiers["Armature"].show_viewport = False
			original.modifiers["Armature"].show_render = False
		bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={
			"linked":False, "mode":'TRANSLATION'}, 
			TRANSFORM_OT_translate={
				"value":(0, 0, 0), 
				"constraint_axis":(False, False, False), 
				"orient_matrix":[[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
				"orient_matrix_type":'GLOBAL',
				"mirror":False, 
				"use_proportional_edit":False, 
				"proportional_edit_falloff":'SMOOTH', 
				"proportional_size":1, 
				"snap":False, "snap_target":'CLOSEST', 
				"snap_point":(0, 0, 0), 
				"snap_align":False, 
				"snap_normal":(0, 0, 0), 
				"gpencil_strokes":False, 
				"texture_space":False, 
				"remove_on_cancel":False, 
				"release_confirm":False, 
				"use_accurate":False
			})
		backup = bpy.context.object
		if setSuffixes == True:
			if workingSuffix in backup.name:
				originalname = backup.name.replace(workingSuffix, '')
			else:
				backup.name = originalname + workingSuffix
		else:
			backup.name = originalname
		remove_shape_keys(original)
		apply_modifiers(original)
		if bpy.context.object.data.shape_keys:
			for key, shape_key in get_active_block().items():
				if shape_key.name == "Basis":
					print ("skip")
				else:
					select(backup)
					bpy.ops.object.duplicate_move(
						OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, 
						TRANSFORM_OT_translate={
							"value":(0, 0, 0), 
							"constraint_axis":(False, False, False), 
							"orient_matrix":[[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
							"orient_matrix_type":'GLOBAL',
							"mirror":False, 
							"use_proportional_edit":False, 
							"proportional_edit_falloff":'SMOOTH', 
							"proportional_size":1, 
							"snap":False, 
							"snap_target":'CLOSEST', 
							"snap_point":(0, 0, 0), 
							"snap_align":False, 
							"snap_normal":(0, 0, 0), 
							"gpencil_strokes":False, 
							"texture_space":False, 
							"remove_on_cancel":False, 
							"release_confirm":False, 
							"use_accurate":False
						})
					meshed_shape_key = bpy.context.object
					select(meshed_shape_key)
					reset_shape_keys()
					get_active_block()[key].value = 1
					bpy.ops.object.convert(target='MESH')
			
					select(original)
					meshed_shape_key.select_set(True)
					bpy.ops.object.join_shapes()
					select_last_shape_key()
					bpy.context.object.active_shape_key.name = key
			
					select(meshed_shape_key)
					bpy.ops.object.delete(use_global=False)
					# setting the active shapekey
					#iIndex = oObject.data.shape_keys.key_blocks.keys().index("Basis.001")
					#oObject.active_shape_key_index = iIndex
					#bpy.ops.object.shape_key_remove()
		if "Armature" in original.modifiers:
			original.modifiers["Armature"].show_viewport = True
			original.modifiers["Armature"].show_render = True
			backup.modifiers["Armature"].show_viewport = True
			backup.modifiers["Armature"].show_render = True
		#original.parent = bpy.data.objects[('Avatar_' + avatarName[0])]
		#bpy.data.collections[(avatarName[0]+'.fbx')].objects.link(original)
		#bpy.data.collections[(avatarName[0]+'_Working')].objects.unlink(original)
		#obj.select_set(False)
