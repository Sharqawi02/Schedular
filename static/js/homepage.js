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
            alert('Event: ' + info.event.title);
            alert('Description: ' + info.event.extendedProps.description);
            info.el.style.borderColor = 'black';
        }
    });

    calendar.render(); // Render the calendar
});
