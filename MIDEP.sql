/*
 Navicat Premium Data Transfer

 Source Server         : localhost ML2iGS3dyqTnisMc
 Source Server Type    : MySQL
 Source Server Version : 80031 (8.0.31)
 Source Host           : localhost:53306
 Source Schema         : MIDEP

 Target Server Type    : MySQL
 Target Server Version : 80031 (8.0.31)
 File Encoding         : 65001

 Date: 03/02/2023 16:21:34
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for article
-- ----------------------------
DROP TABLE IF EXISTS `article`;
CREATE TABLE `article`  (
  `id` bigint NOT NULL,
  `created_at` datetime NULL DEFAULT NULL COMMENT '发布时间',
  `edit_count` int NULL DEFAULT NULL COMMENT '编辑次数',
  `edit_at` datetime NULL DEFAULT NULL COMMENT '编辑时间',
  `show_additional_indication` int NULL DEFAULT NULL COMMENT '显示条件指示',
  `text` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '文章内容',
  `textLength` int NULL DEFAULT NULL COMMENT '文章长度',
  `source` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '文章来源',
  `pic_num` int NULL DEFAULT NULL COMMENT '图片数量',
  `region_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '区域名称',
  `status_title` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '标题',
  `type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '页面类型',
  `page_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '页面URL',
  `page_title` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '页面标题',
  `title` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `content1` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `content2` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `video_orientation` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '视频方向',
  `play_count` int NULL DEFAULT NULL COMMENT '播放次数',
  `reposts_count` int NULL DEFAULT NULL COMMENT '转发数',
  `comments_count` int NULL DEFAULT NULL COMMENT '评论数',
  `reprint_cmt_count` int NULL DEFAULT NULL COMMENT '【未知】',
  `attitudes_count` int NULL DEFAULT NULL COMMENT '点赞数',
  `pending_approval_count` int NULL DEFAULT NULL COMMENT '等待审批数',
  `user` bigint NOT NULL COMMENT '用户',
  `datetime` datetime NULL DEFAULT NULL COMMENT '写入时间',
  `spider_keyword` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '爬虫关键字',
  `server_ip` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '服务器IP',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user`(`user` ASC) USING BTREE,
  CONSTRAINT `article_ibfk_1` FOREIGN KEY (`user`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for media
-- ----------------------------
DROP TABLE IF EXISTS `media`;
CREATE TABLE `media`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `article` bigint NOT NULL COMMENT '微博文章',
  `path` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '文件路径',
  `type` enum('image','video') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'image' COMMENT '文件类型',
  `size` int NULL DEFAULT NULL COMMENT '文件大小',
  `original` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '原地址',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `article`(`article` ASC) USING BTREE,
  CONSTRAINT `media_ibfk_1` FOREIGN KEY (`article`) REFERENCES `article` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 21189 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for task
-- ----------------------------
DROP TABLE IF EXISTS `task`;
CREATE TABLE `task`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `keyword` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '关键字',
  `current` int NULL DEFAULT 1 COMMENT '当前页',
  `page_count` int NULL DEFAULT NULL COMMENT '总页数',
  `priority` int NULL DEFAULT NULL COMMENT '优先级',
  `current_time` datetime NULL DEFAULT NULL COMMENT '当前查询的时间',
  `deadline` datetime NULL DEFAULT NULL COMMENT '查询起始时间',
  `work_start` datetime NULL DEFAULT NULL COMMENT '开始时间',
  `work_end` datetime NULL DEFAULT NULL COMMENT '结束时间',
  `status` int NULL DEFAULT 0 COMMENT '任务状态',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 38 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` bigint NOT NULL,
  `screen_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户名称',
  `profile_image_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '用户头像URL',
  `profile_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '用户主页',
  `statuses_count` int NULL DEFAULT NULL COMMENT '微博数量',
  `verified` int NULL DEFAULT NULL COMMENT '认证状态 boolean',
  `verified_type` int NULL DEFAULT NULL COMMENT '认证类型',
  `verified_type_ext` int NULL DEFAULT NULL COMMENT '【未知】认证相关字段',
  `verified_reason` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '认证说明',
  `close_blue_v` int NULL DEFAULT NULL COMMENT '蓝V boolean',
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '用户描述',
  `gender` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户性别',
  `follow_count` int NULL DEFAULT NULL COMMENT '关注数量',
  `followers_count` int NULL DEFAULT NULL COMMENT '粉丝数量',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
