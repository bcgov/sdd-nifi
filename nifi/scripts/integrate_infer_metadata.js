const args = process.argv.slice(2)
var fs = require('fs');
var inferred_dp_json_str = fs.readFileSync(process.stdin.fd, 'utf-8');
var existing_dp_json_str = args[0];

//integrates a tableschema "field" object with an existing data package's metadata with priority given to existing metadata
function integrate_field_value(field, existing_dp_json) {
	for (var i=0 ; i < existing_dp_json.resources.length; i++){
		resource = existing_dp_json.resources[i];
		for (var j=0 ; j < resource.schema.fields.length; j++){
			if (field.name == resource.schema.fields[j].name){
				if (!(typeof resource.schema.fields[j].rdfType === 'undefined')){
					field.rdfType = resource.schema.fields[j].rdfType;
				}
				field.var_class = resource.schema.fields[j].var_class;
				field.type = resource.schema.fields[j].type;
				field.format = resource.schema.fields[j].format;
				return field;
			}
		}
	}
	return field;
}

//integrates inferred metadata with an existing metadata for the same dataset
function datapackage_integrate_inferred_metadata(inferred_dp_json_str, existing_dp_json_str) {
	try {
		var inferred_dp_json = JSON.parse(inferred_dp_json_str);
		var existing_dp_json = JSON.parse(existing_dp_json_str);
		console.log(JSON.stringify( existing_dp_json ));
		var resource; 
		for (var i=0 ; i < inferred_dp_json.resources.length ; i++)
		{
			resource = inferred_dp_json.resources[i];
			for (var j=0 ; j < resource.schema.fields.length ; j++)
			{
				resource.schema.fields[j] = integrate_field_value(resource.schema.fields[j], existing_dp_json);
			}
		}
		return JSON.stringify(inferred_dp_json, null, 4);
		} catch(err){console.log(err.message); process.exit(1);}
}
try {
    //var existing_dp_json_str = fs.readFileSync('latest_std_edition.json', 'utf8'); 
	console.log(datapackage_integrate_inferred_metadata(inferred_dp_json_str, existing_dp_json_str));	
} catch(e) {
    console.log('Error:', e.stack);
}
