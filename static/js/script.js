document.addEventListener("DOMContentLoaded", function () {
    const starttime = document.getElementById("starttime");
    const endtime = document.getElementById("endtime");

    const now = new Date();
    const today = now.toISOString().slice(0, 16);
    starttime.min = today;

    starttime.addEventListener("input", function () {
        endtime.min = starttime.value;
    });

    const form = starttime.closest("form");
    form.addEventListener("submit", function (event) {
        if (starttime.value >= endtime.value) {
            event.preventDefault();
            alert("Start time must be earlier than end time!");
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const toastElements = document.querySelectorAll('.toast');
    toastElements.forEach(toastElement => {
        const toast = new bootstrap.Toast(toastElement);
        toast.show();
    });
});

document.querySelectorAll('.btn-er-accept').forEach(btn => {
    btn.addEventListener("click", processRequest)
})

document.querySelectorAll('.btn-er-decline').forEach(btn => {
    btn.addEventListener("click", processRequest)
})

function processRequest(event) {
    const btn = event.target.localName === 'button' ? event.target : event.target.parentElement;
    const erId = btn.dataset.erId;
    const endPoint = btn.dataset.erAction === "Accept" ? "accepteventrequest" : "declineeventrequest";
    const resMessage = endPoint === "accepteventrequest" ? "Accepted" : "Declined";

    const btnContainer = btn.parentElement;

    btnContainer.querySelectorAll('button').forEach(btn => btn.disabled = true);

    fetch(`/${endPoint}/${erId}`, { method: "POST" })
        .then(res => res.json())
        .then(res => {
            if (res.message === resMessage) {
                location.reload()
            }
            else {
                alert(res.message);
            }
        })
        .catch(err => {
            alert("Something went wrong!");
        })
        .finally(() => {
            btnContainer.querySelectorAll('button').forEach(btn => btn.disabled = false);
        })
}
