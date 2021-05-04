/*
Works with the approve_import.sh script to handle manual approval of files being brought into the secure zone
Outputs a json with approval information that is feed into the rest of the NiFi flow
The approval information is added to the json that was in the approval queue and then is saved
to an approval folder (so that there's a log of who approved what and when).  The original json file
is then deleted (removing it from the approval queue since it has been approved). 
*/
const args = process.argv.slice(2)
const file_to_approve = args[0];
const current_dir = args[1];
const approver = args[2];
const approval_time = args[3];
const approvaljson = {
  "approver": approver,
  "approval_time": approval_time
}
full_path_to_file_to_approve = current_dir + '/' + file_to_approve
var file_json = require(full_path_to_file_to_approve);
file_json.rz_approval = approvaljson //add in the approval information to json file

const approved_file_location = current_dir + '/approved/' + file_to_approve;
fs = require('fs');
// save the updated json file to an approval folder so that approval is logged
fs.writeFile(approved_file_location, JSON.stringify(file_json, null, 2), function (err) {
  if (err) return console.log(err);
  console.log(file_to_approve + ' has successfully been approved.');
});
//delete original json file (which represents a request for bringing in a data file)
fs.unlink(full_path_to_file_to_approve, (err) => {
  if (err) {
    console.error(err)
    return
  }
  //file removed
})