// import { createContext, useState, useEffect } from "react";
// import axios from "axios";
// import { jwtDecode } from "jwt-decode";

// const AuthContext = createContext();

// export const AuthProvider = ({ children }) => {
//   const [user, setUser] = useState(null);
//   const [isAuthenticated, setIsAuthenticated] = useState(false);
//   const [isLoading, setIsLoading] = useState(true);

//   const api = axios.create({
//     baseURL: "http://localhost:8000/api",
//     headers: { "Content-Type": "application/json" },
//   });

//   api.interceptors.request.use(
//     (config) => {
//       const token = localStorage.getItem("access");
//       const publicEndpoints = ['/home/testimonials/', '/home/testimonials/1/'];
//       if (token && !publicEndpoints.some(endpoint => config.url.includes(endpoint))) {
//         config.headers.Authorization = `Bearer ${token}`;
//       }
//       return config;
//     },
//     (error) => Promise.reject(error)
//   );

//   api.interceptors.response.use(
//     (response) => response,
//     async (error) => {
//       const originalRequest = error.config;
//       if (error.response?.status === 401 && !originalRequest._retry) {
//         originalRequest._retry = true;
//         try {
//           const refreshToken = localStorage.getItem("refresh");
//           const res = await axios.post("http://localhost:8000/api/users/refresh/", {
//             refresh: refreshToken,
//           });
//           const { access } = res.data;
//           localStorage.setItem("access", access);
//           originalRequest.headers.Authorization = `Bearer ${access}`;
//           return api(originalRequest);
//         } catch (refreshError) {
//           logout();
//           return Promise.reject(refreshError);
//         }
//       }
//       return Promise.reject(error);
//     }
//   );

//   useEffect(() => {
//     const initializeAuth = async () => {
//       const token = localStorage.getItem("access");
//       if (token) {
//         try {
//           const decoded = jwtDecode(token);
//           if (decoded.exp * 1000 > Date.now()) {
//             const res = await api.get("/account/account/");
//             setUser(res.data);
//             setIsAuthenticated(true);
//           } else {
//             await refreshToken();
//           }
//         } catch (err) {
//           console.error("Auth initialization failed:", err.response?.data || err.message);
//           logout();
//         }
//       }
//       setIsLoading(false);
//     };
//     initializeAuth();
//   }, []);

//   const login = async (email, password) => {
//     try {
//       const res = await api.post("/users/login/", { email, password });
//       const { access, refresh } = res.data;
//       localStorage.setItem("access", access);
//       localStorage.setItem("refresh", refresh);
//       const decoded = jwtDecode(access);
//       console.log("Token payload:", decoded); // Debug
//       const userRes = await api.get("/account/account/");
//       setUser(userRes.data);
//       setIsAuthenticated(true);
//       return true;
//     } catch (err) {
//       console.error("Login failed:", err.response?.data || err.message);
//       throw err;
//     }
//   };

//   const logout = () => {
//     setUser(null);
//     setIsAuthenticated(false);
//     localStorage.removeItem("access");
//     localStorage.removeItem("refresh");
//   };

//   const refreshToken = async () => {
//     try {
//       const refreshToken = localStorage.getItem("refresh");
//       const res = await axios.post("http://localhost:8000/api/users/refresh/", {
//         refresh: refreshToken,
//       });
//       const { access } = res.data;
//       localStorage.setItem("access", access);
//       const userRes = await api.get("/account/account/");
//       setUser(userRes.data);
//       setIsAuthenticated(true);
//     } catch (err) {
//       console.error("Token refresh failed:", err.response?.data || err.message);
//       logout();
//     }
//   };

//   return (
//     <AuthContext.Provider
//       value={{ user, isAuthenticated, isLoading, login, logout, api }}
//     >
//       {children}
//     </AuthContext.Provider>
//   );
// };

// export default AuthContext;

import { createContext, useState, useEffect } from "react";
import axios from "axios";
import { jwtDecode } from "jwt-decode";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  const api = axios.create({
    baseURL: "http://localhost:8000/api",
    headers: { "Content-Type": "application/json" },
  });

  api.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem("access");
      const publicEndpoints = ["/home/testimonials/", "/home/testimonials/1/"];
      if (token && !publicEndpoints.some((endpoint) => config.url.includes(endpoint))) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => Promise.reject(error)
  );

  api.interceptors.response.use(
    (response) => response,
    async (error) => {
      const originalRequest = error.config;
      if (error.response?.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;
        try {
          const refreshToken = localStorage.getItem("refresh");
          const res = await axios.post("http://localhost:8000/api/users/refresh/", {
            refresh: refreshToken,
          });
          const { access } = res.data;
          localStorage.setItem("access", access);
          originalRequest.headers.Authorization = `Bearer ${access}`;
          return api(originalRequest);
        } catch (refreshError) {
          logout();
          return Promise.reject(refreshError);
        }
      }
      return Promise.reject(error);
    }
  );

  useEffect(() => {
    const initializeAuth = async () => {
      const token = localStorage.getItem("access");
      if (token) {
        try {
          const decoded = jwtDecode(token);
          if (decoded.exp * 1000 > Date.now()) {
            const res = await api.get("/account/account/");
            console.log("Initial user data:", res.data);
            setUser(res.data);
            setIsAuthenticated(true);
          } else {
            await refreshToken();
          }
        } catch (err) {
          console.error("Auth initialization failed:", err.response?.data || err.message);
          logout();
        }
      }
      setIsLoading(false);
    };
    initializeAuth();
  }, []);

  const login = async (email, password) => {
    try {
      const res = await api.post("/users/login/", { email, password });
      const { access, refresh } = res.data;
      localStorage.setItem("access", access);
      localStorage.setItem("refresh", refresh);
      const decoded = jwtDecode(access);
      console.log("Token payload:", decoded);
      const userRes = await api.get("/account/account/");
      console.log("User data:", userRes.data);
      setUser(userRes.data);
      setIsAuthenticated(true);
      return userRes.data; // Return user data for redirection
    } catch (err) {
      console.error("Login failed:", err.response?.data || err.message);
      throw new Error(err.response?.data?.message || "Login failed. Please check your credentials.");
    }
  };

  const logout = () => {
    setUser(null);
    setIsAuthenticated(false);
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
  };

  const refreshToken = async () => {
    try {
      const refreshToken = localStorage.getItem("refresh");
      const res = await axios.post("http://localhost:8000/api/users/refresh/", {
        refresh: refreshToken,
      });
      const { access } = res.data;
      localStorage.setItem("access", access);
      const userRes = await api.get("/account/account/");
      console.log("Refreshed user data:", userRes.data);
      setUser(userRes.data);
      setIsAuthenticated(true);
    } catch (err) {
      console.error("Token refresh failed:", err.response?.data || err.message);
      logout();
    }
  };

  return (
    <AuthContext.Provider
      value={{ user, isAuthenticated, isLoading, login, logout, api }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;