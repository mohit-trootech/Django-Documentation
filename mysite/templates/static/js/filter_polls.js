function submitFilterPollsForm(event) {
  event.preventDefault();
  let orderby = $("#polls-orderby").val();
  let tag = $("#polls-tag").val();

  let updatedPath = `?orderby=${orderby}&tag=${tag}`;
  window.location.href = updatedPath;
}
