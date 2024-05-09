document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        // Your existing calendar configuration
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next',
            center: 'title',
            right: 'multiMonthYear,dayGridMonth,timeGridWeek,timeGridDay,listYear' 
        },
        selectable: true,
        eventSources: [
            // Your existing event source
            {
                url: '/get_events', 
                success: function(data) {
                    var addedEventIds = []; // Array to store IDs of events already added to the calendar

                    data.forEach(event => {
                        if (!addedEventIds.includes(event.id)) {
                            switch (event.priority) {
                                case 'high':
                                    event.backgroundColor = '#b92e34'; 
                                    event.borderColor = '#b92e34'; 
                                    event.textColor = '#000000';
                                    event.color = '#000000'; // Optional: explicitly set text color
                                    break;
                                case 'medium':
                                    event.backgroundColor = '#cd5c5c'; 
                                    event.borderColor = '#cd5c5c'; 
                                    event.textColor = '#000000';
                                    event.color = '#000000'; // Optional: explicitly set text color
                                    break;
                                case 'low':
                                    event.backgroundColor = '#77dd77'; 
                                    event.borderColor = '#77dd77'; 
                                    event.textColor = '#000000';
                                    event.color = '#000000'; // Optional: explicitly set text color
                                    break;
                            }
                            calendar.addEvent(event);
                            addedEventIds.push(event.id);
                        }
                    });
                }
            }
        ],
        eventClick: function(info) {
            var popup = document.getElementById('event-popup');
            var title = document.getElementById('event-title');
            var description = document.getElementById('event-description');
            var date = document.getElementById('event-date');
            var priority = document.getElementById('event-priority');
        
            title.textContent = 'Event: ' + info.event.title;
            description.textContent = 'Description: ' + info.event.extendedProps.description;
            date.textContent = 'Date: ' + info.event.start.toLocaleDateString();
            priority.textContent = 'Priority: ' + info.event.extendedProps.priority;
        
            // Show the popup
            popup.style.display = 'block';
            var viewportWidth = window.innerWidth;
            var viewportHeight = window.innerHeight;
            var popupWidth = popup.offsetWidth;
            var popupHeight = popup.offsetHeight;
            var posX = (viewportWidth - popupWidth) / 2;
            var posY = (viewportHeight - popupHeight) / 2;
            popup.style.left = posX + 'px';
            popup.style.top = posY + 'px';
        
            // Change border color of event element
            info.el.style.borderColor = 'black';
        }
    });

    calendar.render(); // Render the calendar

    // Hide the popup initially
    var popup = document.getElementById('event-popup');
    popup.style.display = 'none';

    // Hide the popup when clicking outside of it
    document.addEventListener('click', function(event) {
        var popup = document.getElementById('event-popup');
        var isClickInsidePopup = popup.contains(event.target);
        var isEventElement = event.target.classList.contains('fc-event') || event.target.parentNode.classList.contains('fc-event');
        if (!isClickInsidePopup && !isEventElement) {
            popup.style.display = 'none';
        }
    });
});
