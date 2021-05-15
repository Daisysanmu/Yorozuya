<template>
  <div>
    <!-- 面包屑导航区 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>我发布的</el-breadcrumb-item>
      <el-breadcrumb-item>我的问题</el-breadcrumb-item>
    </el-breadcrumb>
    <!-- 卡片视图 -->
    <el-card>
      <el-row :gutter="20">
        <el-col :span="4">
          <el-button type="primary" @click="goAddPage">发布问题</el-button>
        </el-col>
      </el-row>

      <!-- 订单列表 -->
      <el-table :data="questionList" border stripe>
        <el-table-column type="index" label="#"></el-table-column>
        <el-table-column label="问题主题" prop="theme" width="600px"></el-table-column>
        <el-table-column label="悬赏金额" prop="reward"></el-table-column>
        <el-table-column label="是否结束">
          <template slot-scope="scope">
            <el-tag type="danger" size="mini" v-if="scope.row.isfinished">已结束</el-tag>
            <el-tag type="success" size="mini" v-else>未结束</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="提问时间" prop="create_time"></el-table-column>
        <el-table-column label="tag" prop="tag" width = "80px"></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button
              v-model="scope.row.isbest"
              size="mini"
              type="info" icon="el-icon-message"
              @click="showAnswerDialog(scope.row.id, scope.row.isfinished)"
            >查看回答</el-button>
          </template>
        </el-table-column>
      </el-table>
      <!-- 分页区域 -->
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="queryInfo.pagenum"
        :page-sizes="[5, 10, 15, 20]"
        :page-size="queryInfo.pagesize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
      ></el-pagination>
    </el-card>
    <el-dialog title="问题答案" :visible.sync="answerDialogVisible" width="75%">
      <!-- 时间线 -->
      <el-table :data="answerList" border stripe>
        <!-- stripe: 斑马条纹
        border：边框-->
        <el-table-column type="index" label="#"></el-table-column>
        <el-table-column prop="username" label="回答者"></el-table-column>
        <el-table-column prop="detail" label="问题答案"></el-table-column>
        <el-table-column label="状态">
          <template slot-scope="scope">
            <el-switch v-model="scope.row.isbest"   :active-value= "1"  :inactive-value= "0" @change="userStateChanged(scope.row)" :disabled="getswitch()" ></el-switch>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
    <el-dialog title="确认赏金" :visible.sync="MoneyVisible" width="25%">
      <el-button type="primary" class="btnAdd" @click="finish()">确认</el-button>
    </el-dialog>
  </div>
</template>

<script>

export default {
  data () {
    return {
      // 分配赏金switch可用状态
      switch: false,
      // 问题id
      q_id: 0,
      // 答案对应用户username
      a_user: '',
      // 我的问题的数量
      total: 0,
      // 问题列表查询参数
      queryInfo: {
        username: window.sessionStorage.getItem('token')
      },
      // 答案列表查询参数
      answerInfo: {
        q_id: 0
      },
      // 分配赏金参数（结束问题）
      endInfo: {
        q_user: window.sessionStorage.getItem('token'),
        a_user: '',
        q_id: 0,
        a_id: 0
      },
      // 订单列表
      questionList: [],
      answerList: [],
      // 修改地址对话框
      addressDialogVisible: false,
      addressForm: {
        address1: [],
        address2: ''
      },
      MoneyVisible: false,
      answerDialogVisible: false
    }
  },
  created () {
    this.getQuestionList()
  },
  methods: {
    // 获取问题列表
    async getQuestionList () {
      const { data: res } = await this.$http.get('http://127.0.0.1:5000/myquestion', {
        params: this.queryInfo
      })
      if (res.meta.status !== 200) {
        return this.$message.error('获取问题列表失败！')
      }
      this.total = res.total
      this.questionList = res.data
    },
    // 获取答案列表
    async showAnswerDialog (id, isfinished) {
      this.switch = isfinished === 1
      this.q_id = id
      this.answerInfo.q_id = id
      this.endInfo.q_id = id
      const { data: res } = await this.$http.get('http://127.0.0.1:5000/getAnswer', {
        params: this.answerInfo
      })
      if (res.meta.status !== 200) {
        return this.$message.error('获取答案列表失败！')
      }
      this.answerList = res.data
      this.answerDialogVisible = true
    },
    // 监听 switch开关 选择某个答案分配赏金 存储当前答案的用户username 并弹出确认显示框
    userStateChanged (answer) {
      this.endInfo['a_user'] = answer['username']
      this.a_user = answer['username']
      this.endInfo['a_id'] = answer['id']
      this.MoneyVisible = true
    },
    // 获取开关状态
    getswitch () {
      return this.switch
    },
    goAddPage () {
      this.$router.push('/addq')
    },
    // 分页
    handleSizeChange (newSize) {
      this.queryInfo.pagesize = newSize
      this.getQuestionList()
    },
    handleCurrentChange (newSize) {
      this.queryInfo.pagenum = newSize
      this.getQuestionList()
    },
    showEditDialog () {
      this.addressDialogVisible = true
    },
    addressDialogClosed () {
      this.$refs.addressFormRef.resetFields()
    },
    async finish () {
      const { data: res } = await this.$http.get('http://127.0.0.1:5000/endQuestion', {
        params: this.endInfo
      })
      if (res.meta.status !== 200) {
        return this.$message.error('提交赏金失败！')
      }
      this.$message.success('提交赏金成功！')
      this.MoneyVisible = false
      this.answerDialogVisible = false
      this.getQuestionList()
    }
  }
}
</script>

<style lang="less" scoped>
.el-cascader {
  width: 100%;
}
</style>
