document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        // this code shows the different views
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next',
            center: 'title',
            right: 'multiMonthYear,dayGridMonth,timeGridWeek,timeGridDay,listYear' 
        },
        selectable: true,
        eventSources: [
            // your event source
            {
                url: '/get_events', 
                success: function(data) {
                    var events = data;
                    events.forEach(function(event) {
                        switch (event.priority) {
                            case 'high':
                                event.backgroundColor = '#cd5c5c'; 
                                event.borderColor = '#cd5c5c'; 
                                event.textColor = '#000000'; 
                                break;
                            case 'medium':
                                event.backgroundColor = '#f0e130'; 
                                event.borderColor = '#f0e130'; 
                                event.textColor = '#000000'; 
                                break;
                            case 'low':
                                event.backgroundColor = '#addfad'; 
                                event.borderColor = '#addfad'; 
                                event.textColor = '#000000'; 
                                break;
                        }
                    });
                    calendar.addEventSource(events);
                }
            }
        ],
        eventClick: function(info) {
            alert('Event: ' + info.event.title);
            alert('Description: ' + info.event.extendedProps.description);
            info.el.style.borderColor = 'black';
        }
    });
    calendar.render();
});
