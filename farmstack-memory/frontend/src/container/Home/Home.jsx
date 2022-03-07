import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import { Container, Grow, Grid, Paper } from '@material-ui/core';

import useStyles from './styles';
import Posts from '../Posts/Posts';
import Form from '../../components/Form/Form';
import Paginate from '../../components/Paginate/Paginate';
import Search from '../../components/Search/Search';

function useQuery() {
  return new URLSearchParams(useLocation().search);
}

const Home = () => {
  const classes = useStyles();
  const [currentId, setCurrentId] = useState(null);

  const query = useQuery();
  const page = query.get('page') || 1;
  const searchQuery = query.get('searchQuery');
  const tags = query.get('tags');

  return (
    <Grow in>
      <Container maxWidth='xl'>
        <Grid container className={classes.gridContainer} justifyContent='space-between'
          alignItems='stretch' spacing={3}
        >
          <Grid item xs={12} sm={6} md={9}>
            <Posts setCurrentId={setCurrentId} />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Search />
            <Form currentId={currentId} setCurrentId={setCurrentId} />
            {(!searchQuery && !tags?.length) && (
              <Paper className={classes.pagination} elevation={6}>
                <Paginate page={page} />
              </Paper>
            )}
          </Grid>
        </Grid>
      </Container>
    </Grow>
  );
}

export default Home;