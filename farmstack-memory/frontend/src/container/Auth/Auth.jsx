import React, { useState } from 'react';
import { Avatar, Button, Paper, Grid, Typography, Container } from '@material-ui/core';
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';

import useStyles from './styles';
import GoogleAuth from './GoogleAuth';
import Input from './Input';
import { signup, signin } from '../../actions/auth';
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';

const initialState = { firstName: '', lastName: '', email: '', password: '', confirmPassword: '' }

const Auth = () => {
  const classes = useStyles();
  const [isSignup, setIsSignup] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState(initialState);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();

    if (isSignup) {
      dispatch(signup(formData, navigate));
    } else {
      dispatch(signin(formData, navigate));
    }
  }

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  }

  const handleShowPassword = () => setShowPassword((prevShowPassword) => !prevShowPassword);

  const switchModel = () => {
    setIsSignup((prevIsSignup) => !prevIsSignup);
    setShowPassword(false);
  }

  return (
    <Container component='main' maxWidth='xs'>
      <Paper className={classes.paper} elevation={3}>
        <Avatar className={classes.avatar}>
          <LockOutlinedIcon />
        </Avatar>
        <Typography variant='h5'>{isSignup ? 'Sign Up' : 'Sign In'}</Typography>
        <form className={classes.form} onSubmit={handleSubmit}>
          <Grid container spacing={2}>
            {
              isSignup && (
                <>
                  <Input name="firstName" label="firstName" handleChange={handleChange}
                    half autoComplete="first-name" />
                  <Input name="lastName" label="lastName" handleChange={handleChange}
                    half autoComplete="last-name" />
                </>
              )
            }
            <Input name="email" label="Email Address" handleChange={handleChange}
              type="email" autoComplete="email" />
            <Input name="password" label="Password" handleChange={handleChange}
              type={showPassword ? 'text' : 'password'} handleShowPassword={handleShowPassword}
              autoComplete="current-password" />
            {isSignup && <Input name="confirmPassword" label="Repeat password" handleChange={handleChange}
              type={showPassword ? 'text' : 'password'} autoComplete="confirm-new-password" />}
          </Grid>
          <Button type="Submit" fullWidth variant="contained" color="primary" className={classes.submit}>
            {isSignup ? 'Sign Up' : 'Sign In'}
          </Button>
          <GoogleAuth />
          <Grid container justifyContent='flex-end'>
            <Grid item>
              <Button onClick={switchModel}>
                {isSignup ? 'Already have account? Sign In' : "Don't have an account? Sign Up"}
              </Button>
            </Grid>
          </Grid>
        </form>
      </Paper>
    </Container>
  );
}

export default Auth;