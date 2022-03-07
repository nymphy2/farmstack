import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { AppBar, TextField, Button } from '@material-ui/core';
import ChipInput from 'material-ui-chip-input';

import useStyles from './styles';
import { getPostsBySearch } from '../../actions/posts';

const Search = () => {
  const classes = useStyles();

  const dispatch = useDispatch();
  const navigate = useNavigate();

  const [searchTerm, setSearchTerm] = useState('');
  const [tags, setTags] = useState([]);

  const searchPost = () => {
    if (searchTerm.trim() || tags) {
      dispatch(getPostsBySearch({ searchTerm, tags: tags.join(',') }))

      navigate(`/posts/search?title=${searchTerm || 'none'}&tags=${tags.join(',')}`);
    } else {
      navigate('/');
    }
  }

  const handleKeyPress = (e) => {
    if (e.keyCode === 13) searchPost();
  }

  const handleAdd = (tag) => setTags([...tags, tag]);

  const handleDelete = (tagToDelete) => setTags(tags.filter((tag) => tag !== tagToDelete));

  return (
    <AppBar className={classes.appBarSearch} position='static' color='inherit'>
      <TextField
        name='search'
        variant='outlined'
        label='Search Posts'
        fullWidth
        value={searchTerm}
        onKeyPress={handleKeyPress}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      <ChipInput
        style={{ margin: '10px 0' }}
        label='Search Tags'
        variant='outlined'
        value={tags}
        onAdd={handleAdd}
        onDelete={handleDelete}
      />
      <Button color='primary' variant='contained' onClick={searchPost}>
        Search
      </Button>
    </AppBar>
  );
}

export default Search;