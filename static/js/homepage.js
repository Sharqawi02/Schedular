document.addEventListener('DOMContentLoaded', function () {

    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {

        // this code shows the diffrent views
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next',
            center: 'title',
            right: 'multiMonthYear,dayGridMonth,timeGridWeek,timeGridDay' // user can switch between the two
        },

        // You can select days with selectable true
        selectable: true,

        eventSources: [

            // your event source
            {
                url: '/get_events', // use the `url` property
                color: '#A63A50',    // an option!
                textColor: 'white'  // an option!
            }

        ],

        eventClick: function (info) {
            paragraphs[0].innerText = 'Event Name: ' + info.event.title
            // change the border color just for fun
            info.el.style.border = '1.5px solid #2c3e50';
        },
        

    });
    calendar.render();
});

