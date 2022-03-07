import React from 'react';
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { GoogleLogin } from 'react-google-login';
import { Button } from '@material-ui/core';

import useStyles from './styles';
import Icon from './Icon';
import { AUTH } from '../../constants/actionTypes';

const GoogleAuth = () => {
  const classes = useStyles();
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const googleSuccess = async (res) => {
    const result = res.profileObj; //undefine
    const token = res?.tokenId;

    // console.log(res);
    // console.log(token);

    try {
      dispatch({ type: AUTH, data: { result, token } });

      navigate('/');
    } catch (error) {
      console.log(error);
    }
  }

  const googleFailure = (error) => {
    console.log(error);
    console.log('Google Sign In was unsuccessful. Try agin later');
  }

  return (
    <>
      <GoogleLogin
        clientId={process.env.REACT_APP_GOOGLE_API_TOKEN}
        render={(renderProps) => (
          <Button
            className={classes.googleButton}
            color='primary'
            fullWidth
            onClick={renderProps.onClick}
            disabled={renderProps.disabled}
            startIcon={<Icon />}
            variant='contained'
          >
            Google Sign In
          </Button>
        )}
        onSuccess={googleSuccess}
        onFailure={googleFailure}
        cookiePolicy='single_host_origin'
      />
    </>
  );
}

export default GoogleAuth;