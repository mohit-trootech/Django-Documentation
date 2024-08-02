function submitFilterPollsForm(event) {
  event.preventDefault();
  let pagnination = $("#polls-perpage").val();
  let orderby = $("#polls-orderby").val();
  let tag = $("#polls-tag").val();

  let updatedPath = `?pagniation=${pagnination}&orderby=${orderby}&tag=${tag}`;
  window.location.href = updatedPath;
}
