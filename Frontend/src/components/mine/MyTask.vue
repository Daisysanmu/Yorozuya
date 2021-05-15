<template>
  <div>
    <!-- 面包屑导航区 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>我发布的</el-breadcrumb-item>
      <el-breadcrumb-item>我的任务</el-breadcrumb-item>
    </el-breadcrumb>
    <!-- 卡片视图 -->
    <el-card>
      <el-row :gutter="20">
        <el-col :span="4">
          <el-button type="primary" @click="goAddPage">发起任务</el-button>
        </el-col>
      </el-row>

      <!-- 订单列表 -->
      <el-table :data="taskList" border stripe>
        <el-table-column type="index" label="#"></el-table-column>
        <el-table-column label="任务主题" prop="theme"></el-table-column>
        <el-table-column label="悬赏金额" prop="reward"></el-table-column>
        <el-table-column label="是否已被承接">
          <template slot-scope="scope">
            <el-tag type="danger" size="mini" v-if="scope.row.isTaken">已有人接受</el-tag>
            <el-tag type="success" size="mini" v-else>未被承接</el-tag>
          </template>
        </el-table-column>

        <el-table-column label="截止时间" prop="ddl"></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button type="success" icon="el-icon-check" size="mini"  @click="finish (scope.row.id)" :disabled="scope.row.isfinished">确认完结</el-button>
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
    <el-dialog title="确认赏金" :visible.sync="MoneyVisible" width="25%">
      <el-button type="primary" class="btnAdd" @click="finish()">确认</el-button>
    </el-dialog>
  </div>
</template>

<script>

export default {
  data () {
    return {
      // 任务列表查询参数
      queryInfo: {
        username: window.sessionStorage.getItem('token')
      },
      // 分配赏金参数（结束问题）
      endInfo: {
        t_id: 0
      },
      total: 0,
      // 任务列表
      taskList: []
    }
  },
  created () {
    this.getTaskList()
  },
  methods: {
    // 获取任务列表
    async getTaskList () {
      const { data: res } = await this.$http.get('http://127.0.0.1:5000/mytask', {
        params: this.queryInfo
      })
      if (res.meta.status !== 200) {
        return this.$message.error('获取我的任务列表失败！')
      }
      this.taskList = res.data
      this.total = res.total
    },
    goAddPage () {
      this.$router.push('/addt')
    },
    // 结束对应任务 分配赏金
    async finish (id) {
      const confirmResult = await this.$confirm(
        '您将结束该任务并分配赏金, 是否继续?',
        '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).catch(err => err)
      // 点击确定 返回值为：confirm
      // 点击取消 返回值为： cancel
      if (confirmResult !== 'confirm') {
        return this.$message.info('已取消')
      }
      this.endInfo['t_id'] = id
      const { data: res } = await this.$http.get('http://127.0.0.1:5000/endTask', {
        params: this.endInfo
      })
      if (res.meta.status !== 200) return this.$message.error('结束任务失败！')
      this.$message.success('确认结束任务成功！')
      this.getTaskList()
    }
  }
}
</script>

<style lang="less" scoped>
.el-cascader {
  width: 100%;
}
</style>
