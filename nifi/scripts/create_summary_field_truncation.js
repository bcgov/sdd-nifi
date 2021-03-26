const args = process.argv.slice(2)
var fs = require('fs');
var dp_json_str = fs.readFileSync(process.stdin.fd, 'utf-8');

// creates a summary of truncated fields including updated headers
function create_summary_field_truncation(dp_json_str) {
	try {
		var output_str = '';
		var shortened_fields = '';
		var shortened_header = '';
		var dp_json = JSON.parse(dp_json_str);
		for (var i=0 ; i < dp_json.resources.length ; i++)
		{
			resource = dp_json.resources[i];
			shortened_header = shortened_header + resource.name + ' (revised header):\r\n';
			for (var j=0 ; j < resource.schema.fields.length ; j++)
			{
				if (resource.schema.fields[j].name != resource.schema.fields[j].shortname) {
					shortened_fields = shortened_fields + 'resource:' + resource.name + ' field:'+ resource.schema.fields[j].name + ' > ' + resource.schema.fields[j].shortname + '\r\n';
				}
				shortened_header = shortened_header + resource.schema.fields[j].shortname + ',';
			}
			shortened_header = shortened_header.slice(0,shortened_header.length - 2)+'\r\n';
		}
		output_str = output_str + 'List of shortened fields:\r\n';
		output_str = output_str + shortened_fields;
		output_str = output_str + '\r\nList of shortened headers:\r\n';
		output_str = output_str + shortened_header;
		return output_str;
		} catch(err){console.log(err.message); process.exit(1);}
}

console.log(create_summary_field_truncation(dp_json_str))