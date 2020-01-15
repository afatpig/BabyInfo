-- Build database
create schema if not exists babyinfo;
use babyinfo;

-- user
create table if not exists `user`(
    id bigint primary key comment 'id',
    username text comment 'base64编码',
    passwdmd5 text comment '密码的md5值',
    email text comment '郵箱，base64',
    `role` text comment '角色，如：管理员admin，员工staff，用户parent等等',
    UNIQUE (username(32))
)CHARSET=utf8mb4 ENGINE=InnoDB;
alter table `user` comment '用户信息';

-- staff
create table if not exists staff(
    id bigint primary key comment 'id，对应user表',
    `name` text comment '名字，不是user里的username，base64编码',
    `name_chs` text comment '中文名字，base64编码',
    gender  text  comment '性别，m=male, f=female',
    group_id    bigint comment '所属group的id',
    INDEX (`name`(32)),
    INDEX (`name_chs`(32))
)CHARSET=utf8mb4 ENGINE=InnoDB;
alter table staff comment '员工信息';

-- child
create table if not exists child(
    id bigint primary key comment 'id，自增',
    `name` text comment 'base64编码',
    `name_chs` text comment 'base64编码',
    `alias` text comment '别名，唯一，可作为username,base64编码',
    gender  text  comment '性别，m=male, f=female',
    religion text  comment '宗教，base64',
    birth_cert_no text comment '出生證號碼',
    born_day date comment '出生日期',
    place_birth text comment '籍貫，base64',
    `address` text comment '住址，base64',
    date_in date comment '入園日期', 
    tel text comment '电话号码',
    email text comment 'email，base64',
    caregiver bigint comment '主要监护人，对应parent的id',
    lang text comment '在家用的语言，base64',
    group_id bigint comment '所属group的id',
    UNIQUE (`alias`(32))
)CHARSET=utf8mb4 ENGINE=InnoDB;
alter table child comment '孩子信息';

-- files
create table if not exists files(
    id bigint auto_increment primary key comment 'id，自增',
    child_id bigint comment '对应孩子的id',
    `filename` text comment '系统内存储时使用的文件名',
    `originfn` text comment '原始文件名，base64编码',
    INDEX (`child_id`)
)CHARSET=utf8mb4 ENGINE=InnoDB;
alter table files comment '文件信息';

-- parent
create table if not exists parent(
    id bigint primary key comment 'id，对应user表',
    `name` text comment '名字base64编码',
    `name_chs` text comment '中文名字base64编码',
    child_ids text comment '孩子id列表，英文逗号隔开',
    relations text comment '关系，base64编码，英文逗号隔开',
    edu text comment '学历，base64编码',
    occupation text comment '职业，base64编码',
    tel text comment '电话号码',
    reason text comment '选择我校的原因，base64编码',
    INDEX (`name`(32)),
    INDEX (`name_chs`(32))
)CHARSET=utf8mb4 ENGINE=InnoDB;
alter table parent comment '家长信息';

-- group
create table if not exists `group`(
    id bigint primary key comment 'id，自增',
    smon int comment '开始月份，包含此月',
    emon int comment '结束月份，包含此月'
)CHARSET=utf8mb4 ENGINE=InnoDB;
alter table `group` comment '组';

-- temperature
create table if not exists `temperature`(
    id bigint auto_increment primary key comment 'id，自增',
    child_id bigint comment '孩子id',
    `time` datetime comment '时间',
    temperature real comment '体温',
    staff_id bigint comment '员工id'
)CHARSET=utf8mb4 ENGINE=InnoDB;
alter table temperature comment '体温';

-- skin
create table if not exists `skin`(
    id bigint auto_increment primary key comment 'id，自增',
    child_id bigint comment '孩子id',
    `time` datetime comment '时间',
    condition_id int comment '皮肤状况id',
    staff_id bigint comment '员工id',
    `count` int comment '数量',
    remark text comment '备注，base64'
)CHARSET=utf8mb4 ENGINE=InnoDB;
alter table skin comment '皮肤检查';

-- condition
create table if not exists `condition`(
    id bigint primary key comment 'id',
    `status` text comment '',
    status_chs text comment '中文status，base64'
)CHARSET=utf8mb4 ENGINE=InnoDB;
alter table `condition` comment '皮肤condition';

-- meal
create table if not exists `meal`(
    id bigint auto_increment primary key comment 'id',
    child_id bigint comment '孩子id',
    `time` datetime comment '时间',
    mealtype int comment '类型的id',
    qty int comment '数量',
    staff_id bigint comment '员工',
    remark text comment '备注，base64'
)CHARSET=utf8mb4 ENGINE=InnoDB;
alter table meal comment '用餐';

-- meal_type
create table if not exists meal_type(
    id bigint primary key comment 'id',
    meal_type text comment 'mealtype',
    meal_type_chs text comment 'mealtype，中文，base64'
)CHARSET=utf8mb4 ENGINE=InnoDB;
alter table meal_type comment '膳食类型';


-- nap
create table if not exists `nap`(
    id bigint auto_increment primary key comment 'id',
    child_id bigint comment '孩子id',
    `time` datetime comment '时间',
    napquality text comment '质量',
    staff_id bigint comment '员工',
    remark text comment '备注，base64'
)CHARSET=utf8mb4 ENGINE=InnoDB;
alter table nap comment '休息';


-- nap_status
create table if not exists `nap_status`(
    id bigint primary key comment 'id',
    napquality text comment '',
    napquality_chs text comment '，base64'
)CHARSET=utf8mb4 ENGINE=InnoDB;
alter table nap_status comment '睡眠质量';


-- diaper
create table if not exists `diaper`(
    id bigint auto_increment primary key comment 'id',
    child_id bigint comment '孩子id',
    `time` datetime comment '时间',
    diaper_id bigint ,
    `count` int,
    staff_id bigint comment '员工',
    remark text comment '备注，base64'
)CHARSET=utf8mb4 ENGINE=InnoDB;
alter table diaper comment '尿布';

-- diaper_status
create table if not exists `diaper_status`(
    id bigint primary key comment 'id',
    `status` text comment '',
    status_chs text comment '中文status，base64'
)CHARSET=utf8mb4 ENGINE=InnoDB;
alter table diaper_status comment '尿布';

-- health
create table if not exists `health`(
    id bigint auto_increment primary key comment 'id',
    child_id bigint comment '孩子id',
    `time` datetime comment '时间',
    health_status_id bigint ,
    staff_id bigint comment '员工',
    remark text comment '备注，base64'
)CHARSET=utf8mb4 ENGINE=InnoDB;
alter table health comment '健康';

-- health status
create table if not exists `health_status`(
    id bigint primary key comment 'id',
    `status` text comment '',
    status_chs text comment '中文status，base64'
)CHARSET=utf8mb4 ENGINE=InnoDB;
alter table health_status comment '健康情况';

-- perform
create table if not exists `perform`(
    id bigint auto_increment primary key comment 'id',
    child_id bigint comment '孩子id',
    `time` datetime comment '时间',
    perform_id bigint ,
    staff_id bigint comment '员工',
    remark text comment '备注，base64'
)CHARSET=utf8mb4 ENGINE=InnoDB;
alter table perform comment '表现';

-- perform detail
create table if not exists `perform_detail`(
    id bigint primary key comment 'id',
    `detail` text comment '',
    detail_chs text comment '中文detail，base64'
)CHARSET=utf8mb4 ENGINE=InnoDB;
alter table perform_detail comment '表现情况';