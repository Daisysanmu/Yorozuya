import Vue from 'vue'
import VueRouter from 'vue-router'

// import Login from '../components/Login.vue'
// import Home from '../components/Home.vue'
// import Welcome from '../components/Welcome.vue'

// import Users from '../components/user/User.vue'
// import Rights from '../components/power/Rights.vue'
// import Roles from '../components/power/Roles.vue'

// import Cate from '../components/goods/Cate.vue'
// import Params from '../components/goods/Params.vue'

// import GoodsList from '../components/goods/List.vue'
// import Add from '../components/goods/Add.vue'

// import Order from '../components/order/Order.vue'
// import Report from '../components/report/Report.vue'

// 路由懒加载
const Login = () => import(/* webpackChunkName: "Login_Home_Welcome" */ '../components/Login.vue')
const Home = () => import(/* webpackChunkName: "Login_Home_Welcome" */ '../components/Home.vue')
const Welcome = () => import(/* webpackChunkName: "Login_Home_Welcome" */ '../components/Welcome.vue')

const Users = () => import(/* webpackChunkName: "Users_Rights_Roles" */ '../components/user/Report.vue')

const QuestionList = () => import(/* webpackChunkName: "Users_Rights_Roles" */ '../components/list/QuestionList.vue')
const TaskList = () => import(/* webpackChunkName: "Cate_Params" */ '../components/list/TaskList.vue')

const Addq = () => import(/* webpackChunkName: "GoodsList_Add" */ '../components/goods/Addq.vue')
const Addt = () => import(/* webpackChunkName: "GoodsList_Add" */ '../components/goods/Addt.vue')

const MyQuestion = () => import(/* webpackChunkName: "Order_Report" */ '../components/mine/MyQuestion.vue')
const MyTask = () => import(/* webpackChunkName: "Order_Report" */ '../components/mine/MyTask.vue')

Vue.use(VueRouter)

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/home',
    component: Home,
    redirect: '/Welcome',
    children: [
      { path: '/home', component: Welcome },
      { path: '/users', component: Users },
      { path: '/questionlist', component: QuestionList },
      { path: '/tasklist', component: TaskList },
      { path: '/addq', component: Addq },
      { path: '/addt', component: Addt },
      { path: '/myquestion', component: MyQuestion },
      { path: '/mytask', component: MyTask }
    ] }

]

const router = new VueRouter({
  routes
})

// 挂载路由导航守卫,to表示将要访问的路径，from表示从哪里来，next是下一个要做的操作 next('/login')强制跳转login
router.beforeEach((to, from, next) => {
  // 访问登录页，放行
  if (to.path === '/login') return next()
  // 获取token
  const tokenStr = window.sessionStorage.getItem('token')
  // 没有token, 强制跳转到登录页
  if (!tokenStr) return next('/login')
  next()
})

export default router
