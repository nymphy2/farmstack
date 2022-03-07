import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Container } from '@material-ui/core';

import Home from './container/Home/Home';
import Navbar from './components/Navbar/Navbar';
import Auth from './container/Auth/Auth';
import PostDetails from './components/PostDetails/PostDetails';

const App = () => {
  const user = JSON.parse(localStorage.getItem('profile'));

  return (
    <Container maxWidth='xl'>
      <Navbar />
      <Routes>
        <Route path='/' element={<Navigate to='/posts' />} />
        <Route path='/posts' element={<Home />} />
        <Route path='/posts/search' element={<Home />} />
        <Route path='/posts/:id' element={<PostDetails />} />
        {!user ? <Route path='/auth' element={<Auth />} /> : <Route path='/auth' element={<Navigate to='/posts' />} />}
      </Routes>
    </Container>
  );
}

export default App;