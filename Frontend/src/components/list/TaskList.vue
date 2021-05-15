<template>
  <div>
    <!-- 面包屑导航区 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>委托浏览</el-breadcrumb-item>
      <el-breadcrumb-item>任务委托</el-breadcrumb-item>
    </el-breadcrumb>
    <!-- 卡片视图 -->
    <el-card>

      <!-- 订单列表 -->
      <el-table :data="orderList" border stripe>
        <el-table-column type="index" label="#"></el-table-column>
        <el-table-column label="任务主题" prop="theme"></el-table-column>
        <el-table-column label="悬赏金额" prop="reward"></el-table-column>
        <el-table-column label="是否已被承接">
          <template slot-scope="scope">
            <el-tag type="danger" size="mini" v-if="scope.row.isTaken">已有人接受</el-tag>
            <el-tag type="success" size="mini" v-else>暂未被承接</el-tag>
          </template>
        </el-table-column>

        <el-table-column label="截止时间" prop="ddl"></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button type="primary" size="mini" icon="el-icon-edit" @click="takeTaskByid (scope.row.id)" :disabled="scope.row.isTaken">接受任务</el-button>
            <el-button
              type="success"
              size="mini"
              icon="el-icon-location"
              @click="showProgressDialog(scope.row.detail)"
            >详情</el-button>
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

    <el-dialog title="委托详细内容" :visible.sync="progressDialogVisible" width="50%">{{detail}}</el-dialog>
  </div>
</template>

<script>

export default {
  data () {
    return {
      // 订单列表查询参数
      queryInfo: {
        query: '',
        pagenum: 1,
        pagesize: 10
      },
      total: 0,
      // 订单列表
      orderList: [],
      // 接受任务的参数
      takeInfo: {
        taskId: 0,
        receiver: window.sessionStorage.getItem('token')
      },
      // 物流进度对话框
      progressDialogVisible: false,
      // 物流进度
      detail: ''
    }
  },
  created () {
    this.getTaskList()
  },
  methods: {
    async getTaskList () {
      console.log(this.queryInfo)
      const { data: res } = await this.$http.get('http://127.0.0.1:5000/taskList', {
        params: this.queryInfo
      })
      if (res.meta.status !== 200) {
        return this.$message.error('获取订单列表失败！')
      }
      this.total = res.data.total
      this.orderList = res.data.taskList
    },
    // 分页
    handleSizeChange (newSize) {
      this.queryInfo.pagesize = newSize
      this.getTaskList()
    },
    handleCurrentChange (newSize) {
      this.queryInfo.pagenum = newSize
      this.getTaskList()
    },
    showEditDialog () {
      this.addressDialogVisible = true
    },
    addressDialogClosed () {
      this.$refs.addressFormRef.resetFields()
    },
    async takeTaskByid (id) {
      const confirmResult = await this.$confirm(
        '您将接受该任务, 是否继续?',
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
      this.takeInfo.taskId = id
      const { data: res } = await this.$http.get('http://127.0.0.1:5000/takeTask', {
        params: this.takeInfo
      })
      if (res.meta.status !== 200) return this.$message.error('接受任务失败！')
      this.$message.success('接受任务成功！')
      this.getTaskList()
    },
    async showProgressDialog (detail) {
      // 供测试的物流单号：1106975712662
      this.detail = detail
      this.progressDialogVisible = true
    }
  }
}
</script>

<style lang="less" scoped>
.el-cascader {
  width: 100%;
}
</style>
