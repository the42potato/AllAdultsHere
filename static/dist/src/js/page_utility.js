/**
 * Copies a string to a user's clipboard.
 * @param {String} content - the string to copy.
 */
async function copy_to_clipboard(content) {
    try {
        await navigator.clipboard.writeText(content)
    }
    catch (err) {
        console.error("Failed to copy text ", err)
    }
}

/**
 * Copies the contents of <label> elements whose associated <input> of type checkbox is in a specified state.
 * @param {EventTarget} elmt - the target element, contained within a <form>.
 * @param {Boolean} [copyUnchecked = false] - whether to copy labels tied to an unchecked checkbox <input>.
 */
function copy_form_checks(elmt, copyUnchecked = false){
    let form = elmt.closest("form"); // closest form will always be the one element is contained inside
    let uncheckedLabels = []

    form.querySelectorAll('input[type="checkbox"]:not(:checked)').forEach(cb => {
        const label = form.querySelector(`label[for="${cb.id}"]`);
        if (label) {
            uncheckedLabels.push(label.textContent.trim());
        }
    });

    console.log("Labels in this form:", uncheckedLabels);
    copy_to_clipboard(uncheckedLabels.join("\n"))
}

// handle clicked elements, running a corresponding function based on
// the element's `data-action` attribute
document.addEventListener("click", e => {
    const action = e.target.dataset.action; // contents of `data-action`
    const element = e.target; // the HTML element itself
    if (action) {
        // if a valid action is found, run its corresponding function
        const action_map = new Map([
            ["copy-form", () => copy_form_checks(element)]
        ])
        selected_action = action_map.get(action);
        if (selected_action) {
            selected_action();
        }
    }
});