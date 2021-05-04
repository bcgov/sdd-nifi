/*
Integrates a inferred metadata (frictionless data package json) with another data package json representing
a previous version of the data.  More specifically, when annual refresh of data is provided, we want
to be able to apply the previous year's classification to this years. Of course there may be differences
between this year's and last year's data, but we want to be able to generate a best guess for the classification
for this year with the understanding that a person would look at and tweak as needed.  
Inferred data has the benefit of finding fields that weren't present in previous years as well as 
dropping of fields that were no longer provided.  Combining inferred with the previous year's metadata gives us 
the best of both worlds
*/
const args = process.argv.slice(2)
var fs = require('fs');
//var inferred_dp_json_str = fs.readFileSync(process.stdin.fd, 'utf-8');
//var existing_dp_json_str = args[0];
//process.env['NODE_CONFIG_DIR'] = args[1];
let config = require('config');
const VAR_CLASS_ATTR = config.get('VAR_CLASS_ATTR');
const RDF_ATTR = config.get('RDF_ATTR');

function isEmptyObject(obj) {
  return !Object.keys(obj).length;
}
function hasFields(resource_obj){
	return !isEmptyObject(resource.schema) && !isEmptyObject(resource.schema.fields);
}
//integrates a tableschema "field" object with an existing data package's metadata with priority given to existing metadata
function integrate_field_value(field, existing_dp_json) {
	for (var i=0 ; i < existing_dp_json.resources.length; i++){
		resource = existing_dp_json.resources[i];
		if (!hasFields(resource)) { continue; }
		for (var j=0 ; j < resource.schema.fields.length; j++){
			if (field.name == resource.schema.fields[j].name){
				if (!(typeof resource.schema.fields[j].rdfType === 'undefined')){
					field[RDF_ATTR] = resource.schema.fields[j][RDF_ATTR];
				}
				field[VAR_CLASS_ATTR] = resource.schema.fields[j][VAR_CLASS_ATTR];
				field.type = resource.schema.fields[j].type;
				field.format = resource.schema.fields[j].format;
				return field;
			}
		}
	}
	return field;
}

//returns an array of objects of {field name :resource name} that are in the resource_1 but not in resource_2
function find_missing_fields_in_resource(resource_1, resource_2) {
	var found = 0;
	var missing_fields = [];
	if (!hasFields(resource_1)) { return missing_fields; }
	for (var j=0 ; j < resource_1.schema.fields.length; j++){
		field = resource_1.schema.fields[j];
		found = 0;
		if (!hasFields(resource_2)) { continue; }
		for (var i=0 ; i < resource_2.schema.fields.length; i++){
			if (field.name == resource_2.schema.fields[i].name){
				found = 1;
				break;
			}
		}
		if (found == 0) { 
			var obj = {}
			obj['resource'] = resource_1.name; 
			obj['field'] = field.name; 
			missing_fields.push(obj); 
		}
	}
	return missing_fields;
}
//finds the missing resources and fields that are present in dp_json_1 but not dp_json_2
//returns and two element array - first element is object array of missing resources (files) , 
// 2nd element is object array of missing field names
//basically we're trying to find the delta between the two metadata files
function find_missing_resources_and_fields_in_datapackage(dp_json_1, dp_json_2) {
	var missing_fields_from_2 = [];
	var missing_resource_from_2 = [];
	var missing_resources_and_fields = [];
	var resource_found = 0;
	for (var i=0 ; i < dp_json_1.resources.length ; i++){
		resource_1 = dp_json_1.resources[i];
		resource_found = 0;
		for (var j=0 ; j < dp_json_2.resources.length ; j++){
			resource_2 = dp_json_2.resources[j];
			if (resource_2.name == resource_1.name){
				resource_found = 1;
				missing_fields_from_2 = find_missing_fields_in_resource(resource_2, resource_1);
			}
		}
		if (resource_found == 0) { missing_resource_from_2.push(resource_1.name); }
	}
	missing_resources_and_fields.push(missing_resource_from_2, missing_fields_from_2);
	return missing_resources_and_fields;
}

//integrates inferred metadata with an existing metadata for the same dataset
function datapackage_integrate_inferred_metadata(inferred_dp_json, existing_dp_json) {
	var resource; 
	for (var i=0 ; i < inferred_dp_json.resources.length ; i++)
	{
		resource = inferred_dp_json.resources[i];
		for (var j=0 ; j < resource.schema.fields.length ; j++)
		{
			resource.schema.fields[j] = integrate_field_value(resource.schema.fields[j], existing_dp_json);
		}
	}
	return inferred_dp_json;
}
try {
	var existing_dp_json_str = fs.readFileSync('latest_std_edition.json', 'utf8'); 
	var inferred_dp_json_str = fs.readFileSync('new_upload.json', 'utf8'); 
	var inferred_dp_json = JSON.parse(inferred_dp_json_str);
	var existing_dp_json = JSON.parse(existing_dp_json_str);
	console.log(JSON.stringify(datapackage_integrate_inferred_metadata(inferred_dp_json, existing_dp_json), null, 4));
	console.log('Missing resources and fields in inferred data');
	var missing_things_from_inferred = find_missing_resources_and_fields_in_datapackage(inferred_dp_json,existing_dp_json);
	if (missing_things_from_inferred[0].length == 0) { console.log('All resources present.'); }
	else { console.log('missing resources: ' + missing_things_from_inferred[0]);}
	if (missing_things_from_inferred[1].length == 0) { console.log('All fields present in matching files.'); }
	else { console.log('missing fields:'); console.log(missing_things_from_inferred[1]);}
	console.log('Missing resources and fields that were in last years data');
	var missing_things_from_existing = find_missing_resources_and_fields_in_datapackage(existing_dp_json,inferred_dp_json);
	if (missing_things_from_existing[0].length == 0) { console.log('All resources present.'); }
	else { console.log('missing resources: ' + missing_things_from_existing[0]);}
	if (missing_things_from_existing[1].length == 0) { console.log('All fields present in matching files.'); }
	else { console.log('missing fields:'); console.log(missing_things_from_existing[1]);}
} catch(e) {
    console.log('Error:', e.stack);
}
