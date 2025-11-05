import React, { useState } from 'react';
import './Register.css';

const Register = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleRegister = async (e) => {
    e.preventDefault();
    const registerResponse = await fetch('http://localhost:8004/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    const registerData = await registerResponse.json();

    if (registerResponse.ok) {
      alert('Registration successful!');

      // Automatically log in the user after successful registration
      const loginResponse = await fetch('http://localhost:8004/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });
      const loginData = await loginResponse.json();

      if (loginResponse.ok) {
        alert('Login successful! Token: ' + loginData.access_token);
        // Store the token in localStorage or state management
        localStorage.setItem('token', loginData.access_token);
      } else {
        alert('Login failed: ' + loginData.detail);
      }
    } else {
      alert('Registration failed: ' + registerData.detail);
    }
  };

  return (
    <div className="register-container">
      <form onSubmit={handleRegister}>
        <h2>Register</h2>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Register</button>
      </form>
    </div>
  );
};

export default Register;