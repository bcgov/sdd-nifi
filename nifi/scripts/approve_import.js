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
file_json.rz_approval = approvaljson

const approved_file_location = current_dir + '/approved/' + file_to_approve;
fs = require('fs');
fs.writeFile(approved_file_location, JSON.stringify(file_json, null, 2), function (err) {
  if (err) return console.log(err);
  console.log(file_to_approve + ' has successfully been approved.');
});
//delete original file
fs.unlink(full_path_to_file_to_approve, (err) => {
  if (err) {
    console.error(err)
    return
  }
  //file removed
})