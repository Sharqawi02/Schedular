document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {

        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next',
            center: 'title',
            right: 'multiMonthYear,dayGridMonth,timeGridWeek,timeGridDay,listYear'
        },

        // You can select events
        selectable: true,

        eventSources: [
            {
                url: '/get_events',
                success: function (data) {
                    return data.map(event => {
                        switch (event.priority) {
                            case 'high':
                                event.backgroundColor = '#c04000';
                                event.borderColor = '#c04000';
                                event.textColor = '#000000';
                                break;
                            case 'medium':
                                event.backgroundColor = '#ffef00';
                                event.borderColor = '#ffef00';
                                event.textColor = '#000000';
                                break;
                            case 'low':
                                event.backgroundColor = '#addfad';
                                event.borderColor = '#addfad';
                                event.textColor = '#000000';
                                break;
                        }
                        return event;
                    });
                }
            }
        ],

        eventClick: function (info) {

            let EventPopupBackground = document.querySelector('.BackgroundForPopupEvents')
            let EventContainer = document.querySelector('.ContainerForPopupEvents')

            EventPopupBackground.classList.add('view')
            EventContainer.classList.add('view')

            EventPopupBackground.addEventListener('click', function() {
                EventPopupBackground.classList.remove('view')
                EventContainer.classList.remove('view')
            })

            document.getElementById('event_id').value = info.event.id;

        }


    });

    calendar.render();

 
});


let EventPopupBackground = document.querySelector('.BackgroundForPopupEvents')
let EventContainer = document.querySelector('.ContainerForPopupEvents')



document.getElementById('open_close').addEventListener('change', function() {
    var asideElement = document.querySelector('.calendar > aside');
    if (this.checked) {
        asideElement.style.display = 'block';
    } else {
        asideElement.style.display = 'none';
    }
});








