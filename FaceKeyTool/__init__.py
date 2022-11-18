bl_info = {
	"name": "FaceKeyTool",
	"blender": (3, 0, 0),
	"category": "Object",
}
from . import SuperApply_function
import bpy
import bmesh
from . import ShapeKeyList
from bpy.types import (
		AddonPreferences,
		Operator,
		Panel,
		)
		
class VIEW3D_PT_AddFaceKeysUI(Panel):
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = "Face Key Tool"
	bl_category = 'Face Key Tool'
	def draw(self, context):
		layout = self.layout
		view = context.space_data
		colbox = layout.box()
		colrow = colbox.row()
		colbox.label(text="Object Tools", icon="OBJECT_DATAMODE")
		colbox.operator("object.addfacekeys", text="Add Face Keys")
		colbox.operator("object.superapply", text="Apply All Modifiers")
		#colbox.prop(context.scene, "MoveToNewCollection", text="Move To Collection")
		colbox.prop(context.scene, "SetSuffixes", text="Add Suffixes to Names")
		if context.scene.SetSuffixes == True:
			colbox.prop(context.scene, "AppliedSuffix", text="Applie Suffix")
			colbox.prop(context.scene, "WorkingSuffix", text="Working Suffix")
		colbox = layout.box()

		colbox.label(text="ShapeKey Tools", icon="SHAPEKEY_DATA")
		colrow = colbox.row()
		colrow.operator("object.createmirrokey", text="Create Mirror Key")
		colrow.prop(context.scene, "UseTopologyMirror", text="Use Topology?")
		colbox.operator("object.transferallshapekeys", text="Transfer All Shape Keys")
		colbox.operator("object.clearselectedverts", text="Clear ShapeKey on Selected Verts")


class VIEW3D_OT_AddFaceKeys(bpy.types.Operator):
	"""AddFaceKeys"""
	bl_idname = "object.addfacekeys"
	bl_label = "AddFaceKeys"
	bl_options = {'REGISTER', 'UNDO'}		
	def execute(self, context):
		obj = bpy.context.active_object
		#ShapeKeyList stored in ShapeKeyList.py
		Keylist= ShapeKeyList.IOSARKITKeylist
		for counter, value in enumerate(Keylist):
			obj.shape_key_add(name = value)
		return {'FINISHED'} 

#Deperecate / For future use
#class VIEW3D_OT_AddDrivers(bpy.types.Operator):
#	"""LinkFaceKeys"""
#	bl_idname = "object.adddrivers"
#	bl_label = "AddDrivers"
#	bl_options = {'REGISTER', 'UNDO'}	
#
#	def execute(self, context):
#		#ShapeKeyList stored in ShapeKeyList.py
#		Keylist= ShapeKeyList.IOSARKITKeylist
#		obj = bpy.context.active_object	
#		shapekey_list_string = str(obj.data.shape_keys.key_blocks.keys())		 
#		for x, key in enumerate(obj.data.shape_keys.key_blocks):
#			print (x, key.name)
#			if key.name in Keylist:
#				skey_driver = key.driver_add('value')
#				skey_driver.driver.type = 'SCRIPTED'
#				skey_driver.driver.expression = '0.0 + var'
#				newVar = skey_driver.driver.variables.new()
#				newVar.name = "var"
#				newVar.type = 'SINGLE_PROP'
#				newVar.targets[0].id_type = 'OBJECT'
#				newVar.targets[0].id = bpy.data.objects['FacekeyTransform_'+key.name]
#				newVar.targets[0].data_path = ('location[0]')
#		return {'FINISHED'} 

				
class VIEW3D_OT_CreateMirrorKey(bpy.types.Operator):
	"""Creates a mirror key of the selected key and automatically names it"""
	bl_idname = "object.createmirrokey"
	bl_label = "CreateMirrorKey"
	bl_options = {'REGISTER', 'UNDO'}	

	def execute(self, context):
		obj = bpy.context.active_object	
		active_key = obj.active_shape_key
		active_key_index = obj.active_shape_key_index
		print (active_key.name)
		keylistlen = len(obj.data.shape_keys.key_blocks)
		bpy.context.object.show_only_shape_key = True
		if "_L" in active_key.name:
			mirroredname = active_key.name.replace("_L", "_R")
		elif "_R" in active_key.name:
			active_key_index -= 1
			mirroredname = active_key.name.replace("_R", "_L")
		elif "Left" in active_key.name:
			mirroredname = active_key.name.replace("Left", "Right")
		elif "Right" in active_key.name:
			active_key_index -= 1
			mirroredname = active_key.name.replace("Right", "Left")
		else:
			mirroredname = (active_key.name + "_Mirrored")
		obj.shape_key_add(name=mirroredname, from_mix=True)
		#mirroredindex = obj.data.shape_keys.key_blocks.find(mirroredname)
		mirroredindex = keylistlen
		obj.active_shape_key_index = mirroredindex
		bpy.ops.object.shape_key_mirror(use_topology=context.scene.UseTopologyMirror)
		bpy.ops.object.shape_key_move(type='TOP')
		for i in range(active_key_index):
			bpy.ops.object.shape_key_move(type='DOWN')

		bpy.context.object.show_only_shape_key = False
		
		
		
		#for x, key in enumerate(obj.data.shape_keys.key_blocks):
		#	print (x, key.name)
		#	 if "_L" in key.name:

		return {'FINISHED'} 
class VIEW3D_OT_TransferAllShapeKeys(bpy.types.Operator):
	"""Transfers All Shape Keys betwen selected objects(Select source object first)"""
	bl_idname = "object.transferallshapekeys"
	bl_label = "Transfer all Shapes"
	bl_options = {'REGISTER', 'UNDO'}	
	def execute(self, context):
		if len(bpy.context.selected_objects) == 2:
			source = bpy.context.selected_objects[1]
			dest = bpy.context.active_object
			for v in bpy.context.selected_objects:
				if v is not dest:
					source = v
					break
			print("Source: ", source.name)
			print("Destination: ", dest.name)
			if source.data.shape_keys is None:
				print("Source object has no shape keys!") 
				self.report({"ERROR"}, "Source object has no shape keys! - Check if you selected in the correct order")
			else:
				for idx in range(1, len(source.data.shape_keys.key_blocks)):
					source.active_shape_key_index = idx 
					print("Copying Shape Key - ", source.active_shape_key.name)
					bpy.ops.object.shape_key_transfer()
		return {'FINISHED'} 

class VIEW3D_OT_SuperApply(bpy.types.Operator):
	"""Applies all modifiers to a new model while retaining its shape keys"""
	bl_idname = "object.superapply"
	bl_label = "Apply all modifiers"
	bl_options = {'REGISTER', 'UNDO'}	
	def execute(self, context):
		setSuffixes = bpy.context.scene.SetSuffixes
		workingSuffix = bpy.context.scene.WorkingSuffix
		appliedSuffix = bpy.context.scene.AppliedSuffix
		SuperApply_function.super_apply_modifiers(workingSuffix, appliedSuffix, setSuffixes)
		return {'FINISHED'} 


class VIEW3D_OT_ClearSelectedVerts(bpy.types.Operator):
	"""Removes all tranforms from the selected verts on the current ShapeKey"""
	bl_idname = "object.clearselectedverts"
	bl_label = "Apply all modifiers"
	bl_options = {'REGISTER', 'UNDO'}	
	def execute(self, context):
		if bpy.context.active_object.mode == "EDIT":
			bpy.ops.mesh.blend_from_shape(shape='Basis', add=False)
		else:
			self.report({"ERROR"}, "Only works in Edit Mode")
		return {'FINISHED'} 


				
bpy.types.Scene.UseTopologyMirror = bpy.props.BoolProperty()
bpy.types.Scene.MoveToNewCollection = bpy.props.BoolProperty()
bpy.types.Scene.SetSuffixes = bpy.props.BoolProperty()
bpy.types.Scene.WorkingSuffix = bpy.props.StringProperty(default = "_Working", name = "Working Suffice", description = "This name will be added to the end of your applied models name - keep empty if you would not like a Suffix")
bpy.types.Scene.AppliedSuffix = bpy.props.StringProperty(default = "_Applied", name = "Applied Suffice", description = "This name will be added to the end of your applied models name - keep empty if you would not like a Suffix")
			
classes = (
			VIEW3D_OT_TransferAllShapeKeys, 
			VIEW3D_OT_AddFaceKeys, 
			VIEW3D_PT_AddFaceKeysUI,
			VIEW3D_OT_CreateMirrorKey,
			VIEW3D_OT_SuperApply,
			VIEW3D_OT_ClearSelectedVerts
			)

def register():
	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)

	
def unregister():
	from bpy.utils import unregister_class
	for cls in reversed(classes):
		unregister_class(cls)