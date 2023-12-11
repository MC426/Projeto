import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Calendar from 'react-calendar'; // Example calendar library, you can choose the one that fits your needs
import 'react-datetime/css/react-datetime.css';
import './ListSchedule.css';
import { useUser } from '../../backendFacade';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const client = axios.create({
  baseURL: "http://localhost:8000"
});

const ScheduleList = () => {
  const { userData, getUser } = useUser();
  const [schedules, setSchedules] = useState([]);
  const [loading, setLoading] = useState(true);
  const [closestEventDate, setClosestEventDate] = useState(null);

  var user_id = null;

  useEffect(() => {
    // Calculate the closest event date when schedules change
    if (schedules.length > 0) {
      const closestDate = new Date(Math.min(...schedules.map(schedule => new Date(schedule.start_ts))));
      setClosestEventDate(closestDate);
    }
  }, [schedules]);


  const tileContent = ({ date, view }) => {
    if (view === 'month') {
      const dateWithoutTime = new Date(date.getFullYear(), date.getMonth(), date.getDate());
      const hasEvent = schedules.some(schedule => {
        const scheduleStart = new Date(schedule.start_ts);
        const scheduleEnd = new Date(schedule.end_ts);
        return dateWithoutTime >= scheduleStart && dateWithoutTime <= scheduleEnd;
      });
      return hasEvent ? <div className="event-day-marker"></div> : null;
    }
    return null;
  };
  

  useEffect(() => {
    const fetchData = async () => {
      await getUser();
      if (userData) {
        user_id = userData.user_id;
      }
      setLoading(false);
      console.log("user_id: ", user_id);
     fetchSchedules(user_id);  
    };
    fetchData();
  }, []);

  const fetchSchedules = (user_id) => {
        if(user_id){

            console.log(user_id);

            client.get("/api/scheduler/list", { withCredentials: true,
                params: { paciente_id: user_id }
            })
            .then(response => {
                setSchedules(response.data);
                setLoading(false);
            })
            .catch(error => {
                console.error("Error fetching schedules:", error);
                setLoading(false);
            });
        }else{
            console.log("User not logged in.");
            setLoading(false);
        }
    };

    return (
      <div style={{ margin: '2%' }}>
        <h2><strong>Suas Consultas:</strong></h2>
        {loading ? (
          <p>Carregando agendas...</p>
        ) : (
          <>
            {schedules.length > 0 ? (
              <>
                <ul>
                  {schedules
                    .slice() // Cria uma cópia do array para não modificar o original
                    .sort((a, b) => a.start_ts - b.start_ts) // Ordena as consultas por data crescente
                    .map((schedule, index) => (
                      <li key={schedule.id}>
                        <strong>Consulta {index + 1}:</strong> {new Date(schedule.start_ts).toLocaleString()} até{' '}
                        {new Date(schedule.end_ts).toLocaleString()}
                        {/* Add additional schedule details as needed */}
                      </li>
                    ))}
                </ul>
                {/* Example: Display schedules in a calendar */}
                <div>
                  <Calendar value={closestEventDate} tileContent={tileContent} />
                  {/* Configure calendar settings based on your library's documentation */}
                  {/* Example: events={schedules.map(schedule => new Date(schedule.start_ts))} */}
                </div>
              </>
            ) : (
              <p style = {{fontSize : '20px'}}>Nenhuma consulta marcada.</p>
            )}
          </>
        )}
      </div>

      );
    
};

export default ScheduleList;