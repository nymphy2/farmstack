import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { Card, CardActions, CardContent, CardMedia, Button, Typography, ButtonBase } from '@material-ui/core';
import DeleteIcon from '@material-ui/icons/Delete';
import MoreHorizIcon from '@material-ui/icons/MoreHoriz';
import moment from 'moment';

import useStyles from './styles';
import Likes from './Likes';
import { deletePost, likePost } from '../../actions/posts';

const Post = ({ post, setCurrentId }) => {
  const classes = useStyles();
  const [likes, setLikes] = useState(post?.likes);

  const dispatch = useDispatch();
  const navigate = useNavigate();

  const user = JSON.parse(localStorage.getItem('profile'));
  const userId = user?.result?.googleId || user?.result?._id;
  // const hasLikedPost = likes.find((like) => like === userId)
  const hasLikedPost = likes.find((like) => like === userId);

  const openPost = () => navigate(`/posts/${post._id}`);

  const handleLike = () => {
    dispatch(likePost(post._id));

    if (hasLikedPost) {
      setLikes(likes.filter((id) => id !== userId));
    } else {
      setLikes([...likes, userId]);
    }
  }

  return (
    <Card className={classes.card} raised elevation={6}>
      <ButtonBase className={classes.cardAction} onClick={openPost}>
        <CardMedia className={classes.media} image={post.selectedFile} title={post.title} />
        <div className={classes.overlay}>
          <Typography variant='h6'>{post.name}</Typography>
          <Typography variant='body2'>{moment(post.createdAt).fromNow()}</Typography>
        </div>
      </ButtonBase>
      {(user?.result?.googleId === post.creator || user?.result?._id === post.creator) && (
        <div className={classes.overlay2}>
          <Button style={{ color: 'white' }} size='small' onClick={() => setCurrentId(post._id)}>
            <MoreHorizIcon fontSize='medium' />
          </Button>
        </div>
      )}
      <ButtonBase className={classes.cardAction} onClick={openPost}>
        <div className={classes.details}>
          <Typography variant='body2' color='textSecondary' >
            {post.tags.map((tag) => `#${tag}`)}
          </Typography>
        </div>
        <Typography className={classes.title} variant='h5' gutterBottom>{post.title}</Typography>
        <CardContent>
          <Typography variant='body2' color='textSecondary' component='p'>{post.message}</Typography>
        </CardContent>
      </ButtonBase>

      <CardActions className={classes.cardActions}>
        <Button size='small' color='primary' disabled={!user?.result} onClick={handleLike}>
          <Likes likes={likes} hasLikedPost={hasLikedPost} />
        </Button>
        {(user?.result?.googleId === post.creator || user?.result?._id === post.creator) && (
          <Button size='small' color='primary' onClick={() => dispatch(deletePost(post._id))}>
            <DeleteIcon fontSize='small' />
            Delete
          </Button>
        )}
      </CardActions>
    </Card>
  );
}

export default Post;