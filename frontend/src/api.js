const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api';

function getToken(){ return localStorage.getItem('token'); }
export function setToken(t){ localStorage.setItem('token', t) }
export function clearToken(){ localStorage.removeItem('token') }

async function request(path, {method='GET', body, auth=true}={}){
  const headers = { 'Content-Type':'application/json' };
  if(auth && getToken()) headers['Authorization'] = 'Bearer ' + getToken();
  const res = await fetch(API_BASE + path, { method, headers, body: body ? JSON.stringify(body) : undefined });
  if(res.status === 204) return null;
  const data = await res.json().catch(()=>({}));
  if(!res.ok){ throw new Error(data.detail || 'Request failed'); }
  return data;
}

export const api = {
  login: (username, password) => request('/auth/token/', {method:'POST', body:{username,password}, auth:false}),
  register: (payload) => request('/auth/register/', {method:'POST', body:payload, auth:false}),
  me: () => request('/me/'),
  updateMe: (payload) => request('/me/', {method:'PATCH', body:payload}),
  universities: () => request('/universities/',{auth:false}),
  users: (q='') => request('/users/?search='+encodeURIComponent(q)),
  courses: () => request('/courses/'),
  createCourse: (payload) => request('/courses/', {method:'POST', body:payload}),
  enroll: (courseId) => request(`/courses/${courseId}/enroll/`, {method:'POST'}),
  enrollments: () => request('/enrollments/'),
  groups: () => request('/groups/'),
  createGroup: (payload) => request('/groups/', {method:'POST', body:payload}),
  addMember: (groupId, userId) => request(`/groups/${groupId}/add_member/`, {method:'POST', body:{user_id:userId}}),
  projects: () => request('/projects/'),
  createProject: (payload) => request('/projects/', {method:'POST', body:payload}),
  tasks: () => request('/tasks/'),
  createTask: (payload) => request('/tasks/', {method:'POST', body:payload})
}
