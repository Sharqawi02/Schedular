document.addEventListener('DOMContentLoaded', function () {

    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {

        // this code shows the diffrent views
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next',
            center: 'title',
            right: 'multiMonthYear,dayGridMonth,timeGridWeek,timeGridDay,listYear' // user can switch between the two
        },

        // You can select days with selectable true
        selectable: true,

        eventSources: [

            // your event source
            {
                url: '/get_events', // use the `url` property
                color: '#ffdffa',    // an option!
                textColor: 'black'  // an option!
            }

        ],

        eventClick: function(info) {
            alert('Event: ' + info.event.title);
            alert('Description: ' + info.event.extendedProps.description);
        
            // change the border color just for fun
            info.el.style.borderColor = 'black';
          },

        

    });
    calendar.render();
});

