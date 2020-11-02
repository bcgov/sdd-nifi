const args = process.argv.slice(2)
const file_to_approve = args[0];
const approver = args[1];
const approval_time = args[2];
const approvaljson = {
  "approver": approver,
  "approval_time": approval_time
}

var file_json = require("./" + file_to_approve);
file_json.rz_approval = approvaljson
//console.log(JSON.stringify(file_json, null, 2));
const approved_file_location = './approved/' + file_to_approve;
fs = require('fs');
fs.writeFile(approved_file_location, JSON.stringify(file_json, null, 2), function (err) {
  if (err) return console.log(err);
  console.log(file_to_approve + ' has successfully been approved.');
});