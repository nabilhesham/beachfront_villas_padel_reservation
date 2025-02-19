// Convert to local datetime and format as 'YYYY-MM-DDTHH:mm:ss' without timezone
function formatDate(date) {
    let year = date.getFullYear();
    let month = String(date.getMonth() + 1).padStart(2, '0');
    let day = String(date.getDate()).padStart(2, '0');
    let hours = String(date.getHours()).padStart(2, '0');
    let minutes = String(date.getMinutes()).padStart(2, '0');
    let seconds = String(date.getSeconds()).padStart(2, '0');
    return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}`;
}

function formatDateString(dateInput) {
  const date = new Date(dateInput);
  // const day = date.toLocaleString('en-US', { weekday: 'short' }); // e.g., "Fri"
  const day = date.toLocaleString('fr-FR', { weekday: 'short' }); // e.g., "Fri"
  const month = date.getMonth() + 1; // Months are 0-indexed
  const dayOfMonth = date.getDate(); // Day of the month

  return `${day} ${month}/${dayOfMonth}`;
}

document.addEventListener('DOMContentLoaded', function () {
    initCalendar();
    getPlayerQuota();
});

function initCalendar(){
    // Set Calendar Start & End DateTime
    let start_calendar = new Date(new Date().getTime())
    start_calendar.setHours(start_calendar.getHours());
    start_calendar.setMinutes(0, 0, 0);  // Set minutes, seconds, and milliseconds to 0

    let end_calendar = new Date();
    end_calendar.setHours(start_calendar.getHours() + hoursToDisplayDataInCalendar);
    end_calendar.setMinutes(0, 0, 0);  // Set minutes, seconds, and milliseconds to 0

    // Convert Dates
    let startDate = formatDate(start_calendar);
    let endDate = formatDate(end_calendar);

    const calendarEl = document.getElementById('calendar');

    if (calendar) {
        calendar.destroy(); // Destroy the current calendar instance
    }
    calendar = new FullCalendar.Calendar(calendarEl, {
        timeZone: 'local',  // Ensure FullCalendar uses the local timezone
        locale: 'fr',
        initialView: 'timeGrid',
        views: {
            timeGrid: {
                type: 'timeGrid',
                duration: { days: daysToDisplayInCalendar }, // days in view
                buttonText: `${daysToDisplayInCalendar} days`
            },
        },
        headerToolbar: {
            left: '',
            center: 'title',
            right: '',
        },
        allDaySlot: false,
        slotDuration: '01:00:00',
        slotMinTime: '09:00:00', // Start time for each day
        slotMaxTime: '20:00:00', // End time for each day
        nowIndicator: true,
        validRange: {
            start: start_calendar,
            end: end_calendar
        },
        slotLabelContent: function(arg) {
            const startTime = arg.date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            const slotDurationMilliseconds = moment.duration(calendar.getOption('slotDuration')).asMilliseconds();
            const endTime = new Date(arg.date.getTime() + slotDurationMilliseconds);
            const endTimeFormatted = endTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            return { html: `<span>${startTime}-${endTimeFormatted}</span>` };
        },
        loading: function(isLoading) {
            const loader = document.getElementById('calendarLoader'); // Loader element
            if (isLoading) {
                loader.classList.remove('d-none'); // Show loader
                loader.classList.add('d-block'); // Show loader
                loader.offsetHeight; // Trigger a reflow to ensure visibility
            } else {
                loader.classList.add('d-none'); // Hide loader
                 loader.classList.remove('d-block');
            }
        },
        events: function(info, successCallback, failureCallback) {
            // Fetch events (matches) from the backend based on the current visible date range
            fetch(`/api/matches?start_date=${startDate}&end_date=${endDate}`)
            .then(response => response.json())
            .then(data => {
                // create data events
                const events = data.matches.map(match => ({
                    title: `Match`,
                    start: match.start_time,
                    end: match.end_time,
                    extendedProps: {
                        mainPlayers: match.main_players,
                        reservePlayers: match.reserve_players,
                    }
                }));
                successCallback(events);  // Pass the processed events to the calendar
            })
            .catch(error => failureCallback(error));  // Handle errors if needed
        },
        slotLabelFormat: { hour: 'numeric', minute: '2-digit', omitZeroMinute: false },
        eventContent: function(arg) {
            const { event } = arg;

            // block  saturday and sunday matches at 9 AM
            if ((event.start.getDay() === 0 || event.start.getDay() === 6) && event.start.getHours() === 9) {
                let cellHtml = `<div class="fc-event-custom" style="background-color: #000; pointer-events: none;">`
                 cellHtml += `</div>`;
                return {
                    html: cellHtml
                };
            }
            // block all week matches at 13 PM & 14 PM
            if (event.start.getHours() === 13 || event.start.getHours() === 14) {
                let cellHtml = `<div class="fc-event-custom" style="background-color: #000; pointer-events: none;">`
                 cellHtml += `</div>`;
                return {
                    html: cellHtml
                };
            }
            const mainPlayers = event.extendedProps.mainPlayers;
            const reservePlayers = event.extendedProps.reservePlayers;
            let bgColor = 'red'
            if (mainPlayers.length < 4) {
                bgColor = 'green'
            }else if(mainPlayers.length === 4 && reservePlayers.length < 4){
                bgColor = 'yellow'
            }

            const matchStartTime = new Date(event.start); // Match's start time
            const currentTime = new Date(); // Current time
            const timeDifference = matchStartTime - currentTime; // Difference in milliseconds

            // Check if the match is playing Now
            const isMatchPlayingNow = timeDifference <= 0;
            if (isMatchPlayingNow === true){
                bgColor = "#777"
            }

            // construct html content for the cell
            let cellHtml = `<div class="fc-event-custom" style="background-color: ${bgColor};">`

            // check if user registered in the match
            cellHtml += `<span style="width: 10%">`
            if (mainPlayers.includes(user) || reservePlayers.includes(user)){
                cellHtml += `<i class="fa-solid fa-table-tennis-paddle-ball"></i>`
            }
            cellHtml += `</span>`

            if (isMatchPlayingNow === true){
                // cellHtml += `<span style="width: 90%; font-size: 8pt; font-weight: 700;">Playing Now</span>`
                cellHtml += `<span style="width: 90%; font-size: 8pt; font-weight: 700;">En train de jouer</span>`
            }else{
                // cellHtml += `<span style="width: 90%; font-size: 7pt;">Main: <strong>${mainPlayers.length}</strong> - Reserve: <strong>${reservePlayers.length}</strong></span>`
                cellHtml += `<span style="width: 90%; font-size: 7pt;">Principal: <strong>${mainPlayers.length}</strong> - Remplaçant: <strong>${reservePlayers.length}</strong></span>`
            }
            cellHtml += `</div>`;

            return {
                html: cellHtml
            };
        },
        eventClick: function(info) {

            if ((info.event.start.getDay() === 0 || info.event.start.getDay() === 6) && info.event.start.getHours() === 9) {
                // showToast('OFF Time!!!', 'danger');
                showToast('Heures creuses!!!', 'danger');
            } else if (info.event.start.getHours() === 13 || info.event.start.getHours() === 14) {
                // showToast('OFF Time!!!', 'danger');
                showToast('Heures creuses!!!', 'danger');
            } else {

                const matchStartTime = new Date(info.event.start); // Match's start time
                const currentTime = new Date(); // Current time
                const timeDifference = matchStartTime - currentTime; // Difference in milliseconds

                // Time to make the match open for reservation
                const minutesInMillis = MinutesBeforeMatchReservationClose * 60 * 1000; // minutes in milliseconds

                // Check if the match is open for reservation before the next millis minutes
                let isMatchOpenForReservation = timeDifference > minutesInMillis && timeDifference >= 0;

                // Check if the match is playing Now
                const isMatchPlayingNow = timeDifference <= 0;

                // if match main players in not completed the match will still be opened
                if (!isMatchPlayingNow && info.event.extendedProps.mainPlayers.length < 4){
                    isMatchOpenForReservation = true
                };

                openMatchDetailsModal(
                    {
                        title: info.event.title,
                        start: formatDate(info.event.start),
                        end: formatDate(info.event.end),
                        mainPlayers: info.event.extendedProps.mainPlayers,
                        reservePlayers: info.event.extendedProps.reservePlayers,
                        isMatchOpenForReservation: isMatchOpenForReservation,
                        isMatchPlayingNow: isMatchPlayingNow,
                    }
                )
            }
        }
    });

    calendar.render();

    // Refresh data every 1 minute
    const interval = setInterval(function() {
        calendar.refetchEvents();  // Refresh the calendar data
     }, MinutesToRefreshCalendarData * 60 * 1000);
}

// Function to open a modal with match details
function openMatchDetailsModal(matchData) {
    // Create the Main Players table
    const mainPlayersTable = matchData.mainPlayers.length > 0 ?
        matchData.mainPlayers.map(player => `<tr><td>${player}</td></tr>`).join('') :
        '<tr><td></td></tr>';  // If no players, render nothing

    // Create the Reserve Players table
    const reservePlayersTable = matchData.reservePlayers.length > 0 ?
        matchData.reservePlayers.map(player => `<tr><td>${player}</td></tr>`).join('') :
        '<tr><td></td></tr>';  // If no players, render nothing

    // modal HTML
    const modalContent = `
        <div class="modal fade" id="matchDetailsModal" tabindex="-1" aria-labelledby="matchDetailsModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
<!--                        <h5 class="modal-title" id="matchDetailsModalLabel">Match Details</h5>-->
                        <h5 class="modal-title" id="matchDetailsModalLabel">Détails du match</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
<!--                        <h5>Match Details</h5>-->
                        <h5>Détails du match</h5>

                        <!-- Main Players Table -->
                        <table class="table table-bordered table-responsive">
                            <thead>
<!--                                <tr><th class="table-dark">Main Players</th></tr>-->
                                <tr><th class="table-dark">Joueurs principaux</th></tr>
                            </thead>
                            <tbody>
                                ${mainPlayersTable}  <!-- Insert the main players here -->
                            </tbody>
                        </table>

                        <!-- Reserve Players Table -->
                        <table class="table table-bordered table-responsive">
                            <thead>
<!--                                <tr><th class="table-dark">Reserve Players</th></tr>-->
                                <tr><th class="table-dark">Joueurs remplaçants</th></tr>
                            </thead>
                            <tbody>
                                ${reservePlayersTable}  <!-- Insert the reserve players here -->
                            </tbody>
                        </table>

<!--                        <label for="playerType" class="form-label">Select Reservation Type</label>-->
                        <label for="playerType" class="form-label">Sélectionnez le type de réservation</label>
                        <select id="playerType" class="form-control form-select" style="cursor: pointer;" ${matchData.isMatchOpenForReservation && !matchData.isMatchPlayingNow ? '' : 'disabled'}>
<!--                            <option value="main">Main Player</option>-->
                            <option value="main">Joueur principal</option>
<!--                            <option value="reserve">Reserve Player</option>-->
                            <option value="reserve">Joueur remplaçant</option>
                        </select>
                        <button id="togglePlayerReservationButton" class="btn btn-primary mt-3 w-100" ${matchData.isMatchOpenForReservation && !matchData.isMatchPlayingNow ? '' : 'disabled'}>
<!--                            Click Here to Add/Remove/Switch Player Reservation-->
                            Cliquez ici pour ajouter/supprimer/modifier la réservation d'un joueur
                        </button>
                        <div id="modalLoader" class="d-none text-center mt-3">
                            <div class="spinner-border text-primary" role="status">
<!--                                <span class="visually-hidden">Loading...</span>-->
                                <span class="visually-hidden">Chargement...</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    // init modal event
    document.body.insertAdjacentHTML('beforeend', modalContent);
    modal = new bootstrap.Modal(document.getElementById('matchDetailsModal'));
    modal.show();

    // toggle player reservation event
    document.getElementById('togglePlayerReservationButton').addEventListener('click', function () {
        const playerType = document.getElementById('playerType').value;
        togglePlayer(matchData, playerType);
    });

    // remove modal event
    document.getElementById('matchDetailsModal').addEventListener('hidden.bs.modal', function () {
        document.getElementById('matchDetailsModal').remove();
    });
}

function togglePlayer(matchData, playerType) {
    // init loader
    const modal_loader = document.getElementById('modalLoader');
    modal_loader.classList.remove('d-none');  // Show loader
    document.getElementById('togglePlayerReservationButton').disabled = true;

    fetch(TogglePlayerReservationURL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRF_TOKEN,
        },
        body: JSON.stringify({
            match_start: matchData.start,
            match_end: matchData.end,
            player_type: playerType,
        })
    })
    .then(response => response.json())
    .then(async (response) => {
        if ('error' in response){
            showToast(response.error, 'danger');
        }
        await modal_loader.classList.add('d-none');  // Hide loader
        await modal.hide();  // Close the modal
        initCalendar();
        getPlayerQuota();
    }).catch(error => alert('Error updating player: ' + error))
}


function getPlayerQuota() {
    // Show loader and hide content initially
    const loader = document.getElementById("quota-content-loader");
    const quotaContent = document.getElementById("quota-content");

    // API URL
     // Replace with your actual API endpoint
    // Fetch data from the API
    fetch(UserReservationQuotaURL)
        .then((response) => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json(); // Parse the JSON response
        })
        .then((data) => {
            // Hide loader
            loader.style.display = "none";
            quotaContent.style.display = "flex";

            // // Populate HTML with the data
            document.getElementById("user-main-quota").textContent = `${data.user_busy_hour_main_reservations.length}/${AllowedUserBusyHourMainReservations}`;
            document.getElementById("user-reserve-quota").textContent = `${data.user_busy_hour_reserve_reservations.length}/${AllowedUserBusyHourReserveReservations}`;
            document.getElementById("total-main-quota").textContent = `${data.villa_busy_hour_main_reservations.length}/${AllowedTotalBusyHourMainReservations}`;
            document.getElementById("total-reserve-quota").textContent = `${data.villa_busy_hour_reserve_reservations.length}/${AllowedTotalBusyHourReserveReservations}`;
            // document.getElementById("start-end-week").textContent = `from ${formatDateString(data.week_start)} to ${formatDateString(data.week_end)}`;
            document.getElementById("start-end-week").textContent = `de ${formatDateString(data.week_start)} à ${formatDateString(data.week_end)}`;
        })
        .catch((error) => {
            // Handle errors (e.g., network issues, API errors)
            console.error("Error fetching quota data:", error);
            loader.textContent = "Failed to load data.";
        });
}
