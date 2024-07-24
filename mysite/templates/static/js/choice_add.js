$(document).ready(() => {
  $("#choiceAdd").on("click", (event) => {
    event.preventDefault();
    let choiceInput = `<div class="col-md-6 mb-3">
                <input type="text" class="form-control" id="choiceText" name="choices" placeholder="Please Enter Choice Text" required>
                <div class="invalid-feedback">
                    Please Enter Choice Text
                </div>
                <div class="valid-feedback">
                    Looks good!
                </div>
            </div>`;
    $("#choicesInput").append(choiceInput);
  });
});
