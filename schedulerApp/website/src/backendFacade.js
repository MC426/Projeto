import React, { createContext, useContext, useState } from 'react';
import axios from 'axios';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const client = axios.create({
  baseURL: "http://localhost:8000"
});


const UserContext = createContext();

export const BackendFacade = ({children}) => {
    const [userData, setUserData] = useState(null);

    const updateUserData = (newData) => {
        setUserData(newData);
    };

    const getUser = () => {
        client.get("/api/user", 
        {
          withCredentials: true
        })
          .then(function (res) {
            if (res.data && res.data.email) {
              console.log("conseguiu logar", res.data);
              updateUserData(res.data);
            }
          })
          .catch(function (error) {
            console.log("nao conseguiu o id do usuario");
          });
      return userData;
    };
    const loginUser = ({email, password}) => {
      console.log("tentando logar: ", email, password)
        client.post("/api/login", {
            email: email,
            password: password
        }, {
            withCredentials: true
        })
        .then(function (res) {
          console.log(res.status);
          console.log("cheguei aqui: ", res.data);
            if (res.status == 200) {
                console.log("conseguiu logar", res.data.is_doctor);
                updateUserData(res.data);
            }
        })
        .catch(function (error) {
            console.log("nao conseguiu logar");
        });
    }
    const logoutUser = () => {
        client.post("/api/logout", {}, {
            withCredentials: true
        })
        .then(function (res) {
            if (res.status === 204 || res.status==200) {
                console.log("conseguiu deslogar");
                updateUserData(null);
              }
        })
        .catch(function (error) {
            console.log("nao conseguiu deslogar");
        });
    }
    const registerUser = ({email, username, password}) => {
        client.post(
            "/api/register",
            {
                email: email,
                username: username,
                password: password
            }
            ).then(function(res) {
            client.post(
                "/api/login",
                {
                email: email,
                password: password
                }
            ).then(function(res) {
              console.log(res.data);
              setUserData(res.data);
              const token = res.data.jwt
              document.cookie = `jwt=${token}; path=/`;
            }).catch(function(error){
              console.log("Error");
            });
        });
    }

    function getUserById(id) {
      return client.get(
        "/api/user-id",
        {
          params: {id: id}
        }
      )
    }

    function createRoomReservation(roomId, startTime, endTime) {
      return client.post(
        "/api/scheduler/manage-room-reservations",
        {
          room_name: roomId,
          medico: userData.user_id,
          start_ts: startTime,
          end_ts: endTime
        }
      )
    }

    function getRoomReservations(medicoId) {
      return client.get(
        "/api/scheduler/manage-room-reservations",
        {
          params: {medico: medicoId}
        }
      )  
    }

    function deleteReservation(id) {
      return client.delete(
        "/api/scheduler/manage-room-reservations",
        {
          params: {id: id}
        }
      )
    }

    function getRooms() {
      return client.get(
        "/api/scheduler/manage-rooms"
      )
    }

    return (
        <UserContext.Provider value={{userData, getUser, loginUser, registerUser, logoutUser,
        getUserById, createRoomReservation, getRoomReservations, deleteReservation, getRooms,
        deleteReservation}}>
          {children}
        </UserContext.Provider>
      );
};

export const useUser = () => {
    return useContext(UserContext);
};  