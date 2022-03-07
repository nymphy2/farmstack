import {
  FETCH_ALL,
  FETCH_POST,
  FETCH_BY_SEARCH,
  CREATE,
  UPDATE,
  DELETE,
  COMMENT,
  START_LOADING,
  END_LOADING
} from '../constants/actionTypes';

const postsReducer = (state = { isLoading: true, posts: [] }, action) => {
  switch (action.type) {
    case START_LOADING:
      return { ...state, isLoading: true }
    case END_LOADING:
      return { ...state, isLoading: false }
    case FETCH_POST:
      return { ...state, post: action.payload }
    case FETCH_ALL:
      return {
        ...state,
        posts: action.payload.data,
        currentPage: action.payload.currentPage,
        numberOfPages: action.payload.numberOfPages,
      }
    case FETCH_BY_SEARCH:
      return { ...state, posts: action.payload }
    case CREATE:
      return { ...state, posts: [...state.posts, action.payload] }
    case UPDATE:
      return {
        ...state,
        posts: state.posts.map((post) => post._id === action.payload._id ? action.payload : post),
      }
    case DELETE:
      return { ...state, posts: state.posts.filter((post) => post._id !== action.payload) }
    case COMMENT:
      return {
        ...state,
        posts: state.posts.map((post) => {
          //change the post received comment
          if (post._id === action.payload._id) return action.payload;

          //return all other post normally
          return post;
        }),
      }
    default:
      return state;
  }
}

export default postsReducer;