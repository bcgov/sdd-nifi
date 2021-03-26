const args = process.argv.slice(2)
var fs = require('fs');
var dp_json_str = fs.readFileSync(process.stdin.fd, 'utf-8');
const DEFAULT_MAX_FIELD_LENGTH = 32
var max_field_length = args[0] > 0 ? args[0]: DEFAULT_MAX_FIELD_LENGTH;

//check uniqueness of purposed shortened field name; want to avoid conflicts with other field's names and shortnames
function check_field_name_uniqueness(resource_fields, purposed_name){
	for (var k=0; k < resource_fields.length; k++) {
		if (resource_fields[k]["name"] == purposed_name || resource_fields[k]["shortname"] == purposed_name) {
			return false;
		}
	}
	return true;
}

//tests if a purposed shortened field name is unique and if not tries adding numbers to the name to make it unique
function generate_unique_field_name(resource_fields, purposed_name) {
	if (check_field_name_uniqueness(resource_fields, purposed_name)) {
		return purposed_name;
	}
	else {
		purposed_name = purposed_name.slice(0,purposed_name.length-1);
		for (var l=0; l < 10; l++) {
			purposed_name = purposed_name.slice(0,purposed_name.length-1) + l;
			if (check_field_name_uniqueness(resource_fields, purposed_name)) {
				return purposed_name;
			}
		}
		console.log('Cannot shorten fields without creating duplicate names. Field:'+ purposed_name); process.exit(1);
	}
}

//truncates data package json resouce schema field names to a set length
function datapackage_truncate_fields(dp_json_str, max_field_length) {
	try {
		var dp_json = JSON.parse(dp_json_str);
		var field_short_name;
		for (var i=0 ; i < dp_json.resources.length ; i++)
		{
			resource = dp_json.resources[i];
			for (var j=0 ; j < resource.schema.fields.length ; j++)
			{
				field = resource.schema.fields[j];
				field_short_name = field["name"].slice(0,max_field_length);
				field["shortname"] = generate_unique_field_name(resource.schema.fields, field_short_name);
			}
			
		}
		return JSON.stringify(dp_json, null, 4);
		} catch(err){console.log(err.message); process.exit(1);}
}

console.log(datapackage_truncate_fields(dp_json_str, max_field_length));