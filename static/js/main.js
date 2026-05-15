document.addEventListener("DOMContentLoaded", function () {

    // access portal
    // disable sign up link for patient
    const signup = document.getElementById("signUp");
    const pat = document.getElementById("patient");

    function disableLink(role) {
        if (!signup) return;

        if (role === "patient") {
            signup.style.display = "none";
            pat.style.display = "block";
        } else {
            signup.style.display = "block";
            pat.style.display = "none";
        }
    }

    // role drop down
    const dropdown = document.querySelector(".dropdown");
    if (dropdown) {
        const select = dropdown.querySelector(".select");
        const caret = dropdown.querySelector(".caret");
        const menu = dropdown.querySelector(".menu");
        const options = dropdown.querySelectorAll(".menu li");
        const selected = dropdown.querySelector(".selected");

        select.addEventListener("click", () => {
            select.classList.toggle("select-clicked");
            caret.classList.toggle("caret-rotate");
            menu.classList.toggle("menu-open");
        });

        options.forEach(option => {
            option.addEventListener("click", () => {
                selected.innerText = option.innerText;

                select.classList.remove("select-clicked");
                caret.classList.remove("caret-rotate");
                menu.classList.remove("menu-open");

                options.forEach(o => o.classList.remove("active"));
                option.classList.add("active");

                disableLink(option.innerText.toLowerCase());
            });
        });

        disableLink(selected.innerText.toLowerCase());

        // close dropdown by clicking outside
        document.addEventListener("click", (e) => {
            if (!dropdown.contains(e.target)) {
                select.classList.remove("select-clicked");
                caret.classList.remove("caret-rotate");
                menu.classList.remove("menu-open");
            }
        });
    }
});

const enterBtn = document.querySelector(".enter-btn");

if (enterBtn) {
    enterBtn.addEventListener("click", () => {
        const selected = document.querySelector(".selected");
        if (!selected) return;

        const role = selected.innerText.toLowerCase();
        window.location.href = `/login?role=${role}`;
    });
}

// =================================================================

// sign up

//validation
const signUpForm = document.getElementById("signup-form");
const signupBtn = document.getElementById("signup-btn");
const emailInput = document.getElementById("email");

if (signUpForm) {
    const passwordInput = document.getElementById("signup-password");
    const pwHint = document.getElementById("pw-hint");
    const username = document.getElementById("signup-username");
    const signupUsernameHint = document.getElementById("signupUsername-hint");

    let isPasswordValid = false;
    let isUsernameValid = false;

    username.addEventListener("input", () => {
        const value = username.value.trim();

        if (value.length >= 3) {
            isUsernameValid = true;
            signupUsernameHint.textContent = "✔ Username looks good.";
            signupUsernameHint.style.color = "green";
        }

        else {
            isUsernameValid = false;
            signupUsernameHint.textContent = "✖ Use at least 3 characters.";
            signupUsernameHint.style.color = "red";
        }
    });


    passwordInput.addEventListener("input", () => {
        const value = passwordInput.value.trim();

        if (value.length >= 15) {
            isPasswordValid = true;
            pwHint.textContent = "✔ Password looks good.";
            pwHint.style.color = "green";
        }

        else {
            isPasswordValid = false;
            pwHint.textContent = "✖ Use at least 15 characters.";
            pwHint.style.color = "red";
        }
    });

    signUpForm.addEventListener("submit", function (event) {

        if (!isUsernameValid || !isPasswordValid) {
            alert("Please ensure all fields are filled correctly.");
            return;
        }
    });
}


//side menu for mobile 
document.addEventListener("DOMContentLoaded", () => {
    const hamburger = document.querySelector(".hamburger");
    const navLinks = document.querySelector(".nav-links");

    if (!hamburger || !navLinks) return;

    hamburger.addEventListener("click", () => {
        hamburger.classList.toggle("active");
        navLinks.classList.toggle("active");
        document.body.classList.toggle("scroll-lock");
    });

    document.addEventListener("click", (e) => {
        if ((!navLinks.contains(e.target)) && (!hamburger.contains(e.target))) {
            e.stopPropagation;
            navLinks.classList.remove("active");
            hamburger.classList.remove("active");
            document.body.classList.remove("scroll-lock");
        }
    });
});

//=============================================================================================
// Personal Info Pages

//edit info
document.addEventListener("DOMContentLoaded", () => {
    // Edit btn
    document.querySelectorAll(".edit-btn").forEach(button => {
        button.addEventListener("click", () => {
            const form = button.closest(".edit-form");
            if (!form) return;

            const saveBtn = form.querySelector(".save-btn");
            const editBtn = form.querySelector(".edit-btn");
            const cancelBtn = form.querySelector(".cancel-btn");
            const resetBtn = form.querySelector(".reset-btn");
            const editMsg = form.querySelector("#editMsg");

            form.querySelectorAll(".editable").forEach(input => {
                input.disabled = false;
            });

            saveBtn.style.display = "block";
            cancelBtn.style.display = "block";
            resetBtn.style.display = "block";
            editBtn.style.display = "none";
            if (editMsg)
                editMsg.style.display = "block";

        });
    });

    // Cancel btn
    document.querySelectorAll(".cancel-btn").forEach(button => {
        button.addEventListener("click", () => {
            const form = button.closest(".edit-form");
            if (!form) return;

            const saveBtn = form.querySelector(".save-btn");
            const editBtn = form.querySelector(".edit-btn");
            const cancelBtn = form.querySelector(".cancel-btn");
            const resetBtn = form.querySelector(".reset-btn");
            const editMsg = form.querySelector("#editMsg");

            form.reset();

            form.querySelectorAll(".editable").forEach(input => {
                input.disabled = true;
            });

            saveBtn.style.display = "none";
            cancelBtn.style.display = "none";
            resetBtn.style.display = "none";
            editBtn.style.display = "block";
            if (editMsg) editMsg.style.display = "none";
        });
    });

    //Reset btn
    document.querySelectorAll(".reset-btn").forEach(button => {
        button.addEventListener("click", () => {
            const form = button.closest(".edit-form");
            if (!form) return;

            form.querySelectorAll(".editable").forEach(input => {
                input.value = "";
            });
        });
    });
});

//more info button on doctor dashboard
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".more-btn").forEach(button => {
        button.addEventListener("click", () => {
            const infoDiv = button.closest(".information");
            if (!infoDiv) return;
            window.location.href = '/doctor/personal-info';
        }
        );
    });
});


//=============================================================================================
// Doctor-Dashboard Page

//appt block
const filter = document.getElementById("appt-filter");
if (filter) {
    const upcoming = document.getElementById("upcoming-appts");
    const ready = document.getElementById("ready-appts");
    filter.addEventListener("change", () => {
        if (filter.value === "upcoming") {
            upcoming.style.display = "block";
            ready.style.display = "none";
        }
        else {
            upcoming.style.display = "none";
            ready.style.display = "block";
        }
    });
}

//=============================================================================================
// Doctor-Appointment Page

//Open and close book appointment form
function openApptForm() {
    document.getElementById("apptForm").classList.add("show");
    document.body.classList.add("scroll-lock");
}

function closeApptForm() {
    document.getElementById("apptForm").classList.remove("show");
    document.body.classList.remove("scroll-lock");
}

//Book appt form
const bookapptFrom = document.querySelector("#apptForm form");

if (bookapptFrom) {
    bookapptFrom.addEventListener("submit", function (e) {
        const patientId = document.getElementById("pat-id").value.trim().toUpperCase();
        const slot = document.getElementById("slot").value;
        const error = document.getElementById("booking-error");
        const patientIdPattern = /^PAT\d{2}$/;

        if (!slot) {
            e.preventDefault();
            error.textContent = "Please select an appointment slot.";
            return false;
        }

        if (!patientIdPattern.test(patientId)) {
            e.preventDefault();
            error.textContent = "Please enter a valid Patient ID (e.g., PAT01).";
            return false;
        }

        error.textContent = "";
        return true;
    });
}

//filter appt
function filterAppointments() {
    const filter = document.getElementById("apptFilter");
    if (!filter) return;

    const option = filter.value;
    const ready = document.getElementById("readySection");
    const upcoming = document.getElementById("upcomingSection");
    const completed = document.getElementById("completedSection");
    const missed = document.getElementById("missedSection");

    if (ready) ready.style.display = "none";
    if (upcoming) upcoming.style.display = "none";
    if (completed) completed.style.display = "none";
    if (missed) missed.style.display = "none";

    if (option === "ready") {
        ready.style.display = "block";
    }

    if (option === "upcoming") {
        upcoming.style.display = "block";
    }

    if (option === "completed") {
        completed.style.display = "block";
    }

    if (option === "missed") {
        missed.style.display = "block";
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const filter = document.getElementById("apptFilter");
    if (filter) {
        filter.addEventListener("change", filterAppointments);
        filterAppointments();
    }
});



//Selecting rows
let selectedRow = null;
const selectedAppt = document.getElementById("selectedAppointmentId");
const reminder = document.getElementById("reminder");

if (selectedAppt && reminder) {
    document.querySelectorAll(".appt-row").forEach(row => {
        row.addEventListener("click", function (e) {
            e.stopPropagation();

            //remove old row
            if (selectedRow) {
                selectedRow.classList.remove("selected");
            }

            this.classList.add("selected");
            selectedRow = this;

            const appointmentId = this.dataset.id;
            const patientId = this.children[1].innerText;
            const patientName = this.dataset.name;

            // Store values
            selectedAppt.value = appointmentId;
            document.getElementById("modalApptID").value = appointmentId;
            document.getElementById("modalPatID").value = patientId;
            document.getElementById("modalPatName").value = patientName;

            reminder.style.color = "#555";
        });
    });
}

//Unselect row when clicked outside
document.addEventListener("click", function (e) {
    if (!e.target.closest(".appt-row")) {
        if (selectedRow) {
            selectedRow.classList.remove("selected");
            selectedRow = null;
        }

        if (selectedAppt) {
            selectedAppt.value = "";
        }
    }
})

//Mark as completed
function markCompleted() {
    const appt = document.getElementById("selectedAppointmentId").value;
    const reminder = document.getElementById("reminder");

    if (!appt) {
        reminder.style.color = "rgb(166, 16, 16)";
        reminder.style.display = "block";
        return;
    }

    const modal = document.getElementById("addRec");

    modal.querySelectorAll(".consultation-info").forEach(section => {
        section.classList.remove("open");

        const btn = section.querySelector(".plus-btn");
        if (btn) {
            btn.textContent = "+";
            btn.classList.remove("open");
        }
    });

    modal.classList.add("show");
    document.body.classList.add("scroll-lock");

}

//more inputs for diagnosis and prescriptions
document.querySelectorAll(".modal").forEach(modal => {
    modal.querySelectorAll(".consultation-header").forEach(item => {
        item.addEventListener("click", () => {
            const parent = item.closest(".consultation-info");
            const btn = item.querySelector(".plus-btn");

            modal.querySelectorAll(".consultation-info").forEach(section => {
                if (section !== parent) {
                    section.classList.remove("open");

                    const otherBtn = section.querySelector(".plus-btn");
                    if (otherBtn) {
                        otherBtn.textContent = "+";
                        otherBtn.classList.remove("open");
                    }
                }
            });

            parent.classList.toggle("open");

            if (parent.classList.contains("open")) {
                btn.textContent = "-";
                btn.classList.add("open");
            } else {
                btn.textContent = "+";
                btn.classList.remove("open");
            }
        });
    });
});

//validation for record form
function formValidation() {
    const diagnosis = document.querySelector("input[name='diagnosis']").value;
    const prescription = document.querySelector("input[name='prescriptions']").value;
    const error = document.getElementById("record-error");

    if (!diagnosis || !prescription) {
        error.textContent = "Please fill in all fields.";
        return false;
    }

    error.textContent = "";
    return true;
}


function closeRecForm() {
    document.getElementById("addRec").classList.remove("show");
    document.body.classList.remove("scroll-lock");
}

// View appointment details
function openDetailsModal(patient, name, id, date, time, diagnosis, prescription, temp, bp, hr) {
    document.getElementById("d-patient").innerText = patient;
    document.getElementById("d-name").innerText = name;
    document.getElementById("d-id").innerText = id;
    document.getElementById("d-date").innerText = date;
    document.getElementById("d-time").innerText = time;
    document.getElementById("d-diagnosis").innerText = diagnosis || "—";
    document.getElementById("d-prescription").innerText = prescription || "—";
    document.getElementById("d-temp").innerText = temp;
    document.getElementById("d-bp").innerText = bp;
    document.getElementById("d-hr").innerText = hr;

    document.getElementById("detailsModal").classList.add("show");
    document.body.classList.add("scroll-lock");

    const modal = document.getElementById("detailsModal");
    modal.querySelectorAll(".consultation-info").forEach(section => {
        section.classList.remove("open");
        const btn = section.querySelector(".plus-btn");
        if (btn) {
            btn.textContent = "+";
            btn.classList.remove("open");
        }
    });
}

function closeDetailsModal() {
    document.getElementById("detailsModal").classList.remove("show");
    document.body.classList.remove("scroll-lock");
}


//=============================================================================================
// Doctor-Slot Page

// Open and close add slot form
function openSlotForm() {
    document.getElementById("addForm").classList.add("show");
    document.body.classList.toggle("scroll-lock");
}

function closeSlotForm() {
    document.getElementById("addForm").classList.remove("show");
    document.body.classList.remove("scroll-lock");
}

// Open and close edit/book slot form
function openEditOrBookSlot(slotId, date, time) {
    document.getElementById("modalSlotID").value = slotId;
    document.getElementById("modalDate").value = date;
    const formatTime = time.substring(0,5);
    document.getElementById("modalTime").value = formatTime;

    document.getElementById("editOrBook").classList.add("show");
    document.body.classList.toggle("scroll-lock");
}

function closeEditOrBookSlot() {
    document.getElementById("editOrBook").classList.remove("show");
    document.body.classList.toggle("scroll-lock");
}

//Selecting rows
let selection = null;

document.querySelectorAll(".time-block").forEach(row => {
    row.addEventListener("click", function () {
        const slotId = this.dataset.id;
        const date = this.dataset.date;
        const time = this.dataset.time;
        openEditOrBookSlot(slotId, date, time);
    });
});

// edit and book btns
const editBtn = document.getElementById("editBtn");
const saveBtn = document.getElementById("saveBtn");
const cancelBtn = document.getElementById("cancelBtn");
const bookBtn = document.getElementById("bookBtn");
const deleteBtn = document.getElementById("deleteBtn");

const modalDate = document.getElementById("modalDate");
const modalTime = document.getElementById("modalTime");

if (editBtn && saveBtn && cancelBtn && bookBtn && deleteBtn) {
    editBtn.addEventListener("click", function () {
        modalDate.removeAttribute("readonly");
        modalTime.removeAttribute("readonly");

        editBtn.style.display = "none";
        bookBtn.style.display = "none";
        deleteBtn.style.display = "none";
        saveBtn.style.display = "inline-block";
        cancelBtn.style.display = "inline-block";
    });
}

// date and time validation
document.addEventListener("DOMContentLoaded", function () {
    function restrictDateTime(dateInput, timeInput) {
        if (!dateInput || !timeInput) return;
        const today = new Date().toISOString().split("T")[0];
        dateInput.setAttribute("min", today);

        dateInput.addEventListener("change", function () {
            const currentTime = new Date().toTimeString().slice(0, 5);
            const startTime = "08:00";
            const endTime = "17:00";

            let minTime = startTime;
            if (dateInput.value === today && currentTime > startTime) {
                minTime = currentTime;
            }

            timeInput.setAttribute("min", minTime);
            timeInput.setAttribute("max", endTime);
        });

        dateInput.dispatchEvent(new Event("change"));
    }

    restrictDateTime(document.getElementById("modalDate"), document.getElementById("modalTime"));
    restrictDateTime(document.getElementById("slotDate"), document.getElementById("slotTime"));
});


// go to appt pag
if (bookBtn) {
    bookBtn.addEventListener("click", function () {
        const slotID = document.getElementById("modalSlotID").value;
        window.location.href = `/doctor/appointments?slot_id=${slotID}`;
    });
}

//=============================================================================================

// Doctor-Patient Records Page

// Search patient id or name
function patientSearch() {
    const input = document.getElementById('idInput').value.toUpperCase();
    const rows = document.querySelectorAll(".records-table tbody tr");
    const notFound = document.getElementById("notFound");

    if (input === "") {
        rows.forEach(row =>
            row.style.display = ""
        );

        notFound.style.display = "none";
        return;
    }

    let patientFound = false;

    rows.forEach(row => {
        const patId = row.cells[1].textContent.toUpperCase();
        const name = row.cells[2].textContent.toUpperCase();

        if (patId.includes(input) || name.includes(input)) {
            row.style.display = "";
            patientFound = true;
        }

        else {
            row.style.display = "none";
        }
    });

    if (notFound) {
        notFound.style.display = patientFound ? "none" : "block";
    }

}



//=============================================================================================

// Nurse-Patient List Page

// Add patient form
function openAddPatient() {
    document.getElementById("addPatForm").classList.add("show");
    document.body.classList.add("scroll-lock");
}

function closeAddPatient() {
    document.getElementById("addPatForm").classList.remove("show");
    document.body.classList.remove("scroll-lock");
}

//=============================================================================================
// Nurse-Add vitals
function addVitals(appointmentId) {
    window.location.href = "/nurse/add-vitals?appt_id=" + appointmentId;
}

// cancel btn
function cancel() {
    window.location.href = "/nurse/upcoming-appt";
}


//=============================================================================================

// Patient-Medical Records

// Medical record drop down
function expand(element) {
    const dropdown = document.querySelectorAll(".record-dropdown");
    const summary = document.querySelectorAll(".record-sum");
    const selected = element.nextElementSibling;
    const arrow = element.querySelector(".arrow");

    dropdown.forEach(d => {
        if (d !== selected) {
            d.classList.remove("show");
        }
    });

    summary.forEach(info => {
        if (info !== element) {
            info.classList.remove("active");

            const otherArrow = info.querySelector(".arrow");
            if (otherArrow) {
                otherArrow.textContent = "▸";
            }
        }
    })

    selected.classList.toggle("show");
    element.classList.toggle("active");

    if (selected.classList.contains("show")) {
        arrow.textContent = "▾";
    } else {
        arrow.textContent = "▸";
    }
}

//=============================================================================================

// Patient-Appointments


// selecting slot and book btn
let selectedDoct = "";
let selectedDate = "";
let selectedTime = "";

document.addEventListener("DOMContentLoaded", function () {

    const slots = document.querySelectorAll(".slot-block");
    const bookBtn = document.getElementById("bookSlotBtn");
    const selectedSlot = document.getElementById("selectedSlot");

    slots.forEach(slot => {
        slot.addEventListener("click", function (event) {

            event.preventDefault();

            slots.forEach(btn => btn.classList.remove("active"));
            this.classList.add("active");

            // store slot id
            selectedSlot.value = this.dataset.slot;
            selectedDoct = this.dataset.doctor;
            selectedDate = this.dataset.date;
            selectedTime = this.dataset.time;

            bookBtn.style.display = "inline-block";
        });
    });

});

function openBookForm() {
    document.getElementById("thisDoct").innerText = selectedDoct;
    document.getElementById("thisDate").innerText = selectedDate;
    document.getElementById("thisTime").innerText = selectedTime;


    document.getElementById("confirmBooking").classList.add("show");
    document.body.classList.add("scroll-lock");
}

function confirmBooking() {
    document.getElementById("bookApptForm").submit();
}

function cancelBooking() {
    document.getElementById("confirmBooking").classList.remove("show");
    document.body.classList.remove("scroll-lock");
}

//=============================================================================================

// Signing Out
function confirmSignOut(event) {
    event.preventDefault();  // stop link navigation
    document.getElementById("signOut").classList.add("show");

}

function closeConfirmationModal() {
    document.getElementById("signOut").classList.remove("show");
}

function signOut() {
    window.location.href = "/signOut";  // redirect to logout/home
}



//close modal when clicking outside
document.querySelectorAll(".modal").forEach(modal => {
    modal.addEventListener("click", e => {
        if (e.target === modal) {
            modal.classList.remove("show");
        }
    });
});

