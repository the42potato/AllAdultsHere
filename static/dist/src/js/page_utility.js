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
function copyFormChecks(elmt, copyUnchecked = false){
    let form = elmt.closest("form"); // closest form will always be the one element is contained inside
    let uncheckedLabels = []
    query = copyUnchecked ? 'input[type="checkbox"]:not(:checked)' : 'input[type="checkbox"]:checked'

    form.querySelectorAll('input[type="checkbox"]:not(:checked)').forEach(cb => {
        const label = form.querySelector(`label[for="${cb.id}"]`);
        if (label) {
            uncheckedLabels.push(label.textContent.trim());
        }
    });

    copy_to_clipboard(uncheckedLabels.join("\n"))
}

/**
 * Changes the data-timer-status of an element
 * @param {EventTarget} element - the element to apply the change to
 * @param {Number} value - the value to change the element's timer to
 */
function setElementTimer(element, value) {
    element.dataset.timerStatus = value;
}

/**
 * Drives the functionality of the footer character in the links section
 */
function updateFooterChar() {
    let character = document.querySelector("[data-timer-status]");
    if (character) {
        character.dataset.timerStatus--;
        timerStatus = parseInt(character.dataset.timerStatus)
        if (timerStatus % 2 == 0) { // run change every other update (2 * timer interval)
            switch(Math.floor(timerStatus / 2)) { 
                case 0: 
                    console.log("ping!");
                    character.dataset.timerStatus = 10;
            }
        }
    }
}

// handle clicked elements, running a corresponding function based on
// the element's `data-action` attribute
document.addEventListener("click", e => {
    const element = e.target; // the HTML element itself
    const action = element.dataset.clickAction; // contents of `data-action`
    if (action) {
        // if a valid action is found, run its corresponding function
        const action_map = new Map([
            ["copy-form", () => copyFormChecks(element, true)],
            ["footer-character", () => setElementTimer(element, 20)]
        ])
        selected_action = action_map.get(action);
        if (selected_action) {
            selected_action();
        }
    }
});

// Every half second, run updates to parts of the page
const pageTimer = setInterval(() => {
    updateFooterChar()
}, 500)