window.onload = async () => {
  try {
    const user = await axios.get('/checkAuth');
    if (user) window.location.href = '/mypage';
  } catch (e) {
    console.error(e);
  }
};