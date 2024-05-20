document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next',
            center: 'title',
            right: 'multiMonthYear,dayGridMonth,timeGridWeek,timeGridDay,listYear'
        },
        selectable: true,
        eventSources: [
            {
                url: '/get_events',
                success: function (data) {
                    var addedEventIds = [];
                    data.forEach(event => {
                        if (!addedEventIds.includes(event.id)) {
                            switch (event.priority) {
                                case 'high':
                                    event.backgroundColor = '#b92e34';
                                    event.borderColor = '#b92e34';
                                    event.textColor = '#000000';
                                    break;
                                case 'medium':
                                    event.backgroundColor = '#cd5c5c';
                                    event.borderColor = '#cd5c5c';
                                    event.textColor = '#000000';
                                    break;
                                case 'low':
                                    event.backgroundColor = '#77dd77';
                                    event.borderColor = '#77dd77';
                                    event.textColor = '#000000';
                                    break;
                            }
                            calendar.addEvent(event);
                            addedEventIds.push(event.id);
                        }
                    });
                }
            }
        ],
        eventClick: function (info) {
            info.jsEvent.preventDefault(); // Prevent the browser's default action
            showEventPopup(info.event);
        }
    });

    calendar.render();

    var popup = document.getElementById('event-popup');
    popup.style.display = 'none';

    document.addEventListener('click', function (event) {
        if (!popup.contains(event.target) && !event.target.closest('.fc-event')) {
            popup.style.display = 'none';
        }
    });

    function showEventPopup(event) {
        var popup = document.getElementById('event-popup');
        var title = document.getElementById('event-title');
        var description = document.getElementById('event-description');
        var startDate = document.getElementById('event-start-date');
        var endDate = document.getElementById('event-end-date');
        var priority = document.getElementById('event-priority');

        title.textContent = 'Event: ' + event.title;
        description.textContent = 'Description: ' + event.extendedProps.description;
        startDate.textContent = 'Start Date: ' + event.start.toLocaleDateString();
        endDate.textContent = 'End Date: ' + (event.end ? event.end.toLocaleDateString() : 'N/A');
        priority.textContent = 'Priority: ' + event.extendedProps.priority;

        popup.style.display = 'block';
        var viewportWidth = window.innerWidth;
        var viewportHeight = window.innerHeight;
        var popupWidth = popup.offsetWidth;
        var popupHeight = popup.offsetHeight;
        var posX = (viewportWidth - popupWidth) / 2;
        var posY = (viewportHeight - popupHeight) / 2;
        popup.style.left = posX + 'px';
        popup.style.top = posY + 'px';
    }
});
document.addEventListener('DOMContentLoaded', function () {
    var checkbox = document.querySelector('.checkbox');
    var översikt = document.getElementById('översikt');

    checkbox.addEventListener('change', function () {
        if (checkbox.checked) {
            översikt.classList.add('open');
        } else {
            översikt.classList.remove('open');
        }
    });

    document.addEventListener('click', function (event) {
        if (!översikt.contains(event.target) && event.target !== checkbox) {
            checkbox.checked = false;
            översikt.classList.remove('open');
        }
    });
});










