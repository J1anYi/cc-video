/**
 * Internationalization configuration using i18next
 * Supports multiple languages with lazy loading
 */
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

// Translation resources
const resources = {
  en: {
    translation: {
      // Common
      common: {
        loading: 'Loading...',
        error: 'An error occurred',
        retry: 'Retry',
        save: 'Save',
        cancel: 'Cancel',
        delete: 'Delete',
        edit: 'Edit',
        create: 'Create',
        search: 'Search',
        noResults: 'No results found',
        showMore: 'Show more',
        showLess: 'Show less',
      },
      // Navigation
      nav: {
        home: 'Home',
        catalog: 'Catalog',
        login: 'Login',
        register: 'Register',
        logout: 'Logout',
        profile: 'Profile',
        admin: 'Admin',
        settings: 'Settings',
      },
      // Auth
      auth: {
        loginTitle: 'Sign In',
        registerTitle: 'Create Account',
        email: 'Email',
        password: 'Password',
        confirmPassword: 'Confirm Password',
        displayName: 'Display Name',
        forgotPassword: 'Forgot password?',
        noAccount: "Don't have an account?",
        hasAccount: 'Already have an account?',
        loginButton: 'Sign In',
        registerButton: 'Sign Up',
        invalidCredentials: 'Invalid email or password',
        emailSent: 'Password reset email sent',
      },
      // Movies
      movies: {
        title: 'Title',
        description: 'Description',
        category: 'Category',
        releaseYear: 'Release Year',
        duration: 'Duration',
        minutes: 'minutes',
        watchNow: 'Watch Now',
        addToWatchlist: 'Add to Watchlist',
        removeFromWatchlist: 'Remove from Watchlist',
        markFavorite: 'Mark as Favorite',
        unmarkFavorite: 'Remove from Favorites',
        noMovies: 'No movies available',
        categories: {
          action: 'Action',
          comedy: 'Comedy',
          drama: 'Drama',
          horror: 'Horror',
          scifi: 'Science Fiction',
          romance: 'Romance',
          documentary: 'Documentary',
          animation: 'Animation',
        },
      },
      // Ratings & Reviews
      reviews: {
        writeReview: 'Write a Review',
        rating: 'Rating',
        review: 'Review',
        submit: 'Submit Review',
        edit: 'Edit Review',
        delete: 'Delete Review',
        noReviews: 'No reviews yet',
        averageRating: 'Average Rating',
        yourRating: 'Your Rating',
      },
      // Comments
      comments: {
        writeComment: 'Write a comment...',
        submit: 'Post Comment',
        edit: 'Edit',
        delete: 'Delete',
        reply: 'Reply',
        noComments: 'No comments yet',
        loadMore: 'Load more comments',
      },
      // Profile
      profile: {
        title: 'Profile',
        editProfile: 'Edit Profile',
        watchHistory: 'Watch History',
        favorites: 'Favorites',
        watchlist: 'Watchlist',
        followers: 'Followers',
        following: 'Following',
        noHistory: 'No watch history',
        noFavorites: 'No favorites yet',
      },
      // Settings
      settings: {
        title: 'Settings',
        language: 'Language',
        timezone: 'Timezone',
        notifications: 'Notifications',
        emailNotifications: 'Email Notifications',
        pushNotifications: 'Push Notifications',
        saved: 'Settings saved',
      },
      // Errors
      errors: {
        notFound: 'Page not found',
        serverError: 'Server error',
        unauthorized: 'Unauthorized access',
        forbidden: 'Access forbidden',
        networkError: 'Network error. Please check your connection.',
      },
      // Time
      time: {
        justNow: 'Just now',
        minutesAgo: '{{count}} minute ago',
        minutesAgo_other: '{{count}} minutes ago',
        hoursAgo: '{{count}} hour ago',
        hoursAgo_other: '{{count}} hours ago',
        daysAgo: '{{count}} day ago',
        daysAgo_other: '{{count}} days ago',
      },
    },
  },
  zh: {
    translation: {
      // 通用
      common: {
        loading: '加载中...',
        error: '发生错误',
        retry: '重试',
        save: '保存',
        cancel: '取消',
        delete: '删除',
        edit: '编辑',
        create: '创建',
        search: '搜索',
        noResults: '未找到结果',
        showMore: '显示更多',
        showLess: '收起',
      },
      // 导航
      nav: {
        home: '首页',
        catalog: '影片库',
        login: '登录',
        register: '注册',
        logout: '退出登录',
        profile: '个人中心',
        admin: '管理后台',
        settings: '设置',
      },
      // 认证
      auth: {
        loginTitle: '登录',
        registerTitle: '创建账户',
        email: '邮箱',
        password: '密码',
        confirmPassword: '确认密码',
        displayName: '昵称',
        forgotPassword: '忘记密码？',
        noAccount: '还没有账户？',
        hasAccount: '已有账户？',
        loginButton: '登录',
        registerButton: '注册',
        invalidCredentials: '邮箱或密码错误',
        emailSent: '密码重置邮件已发送',
      },
      // 电影
      movies: {
        title: '标题',
        description: '简介',
        category: '分类',
        releaseYear: '上映年份',
        duration: '时长',
        minutes: '分钟',
        watchNow: '立即观看',
        addToWatchlist: '添加到待看列表',
        removeFromWatchlist: '从待看列表移除',
        markFavorite: '收藏',
        unmarkFavorite: '取消收藏',
        noMovies: '暂无影片',
        categories: {
          action: '动作',
          comedy: '喜剧',
          drama: '剧情',
          horror: '恐怖',
          scifi: '科幻',
          romance: '爱情',
          documentary: '纪录片',
          animation: '动画',
        },
      },
      // 评论
      reviews: {
        writeReview: '写评论',
        rating: '评分',
        review: '评论',
        submit: '提交评论',
        edit: '编辑评论',
        delete: '删除评论',
        noReviews: '暂无评论',
        averageRating: '平均评分',
        yourRating: '你的评分',
      },
      // 评论
      comments: {
        writeComment: '写评论...',
        submit: '发表评论',
        edit: '编辑',
        delete: '删除',
        reply: '回复',
        noComments: '暂无评论',
        loadMore: '加载更多评论',
      },
      // 个人中心
      profile: {
        title: '个人中心',
        editProfile: '编辑资料',
        watchHistory: '观看历史',
        favorites: '收藏',
        watchlist: '待看列表',
        followers: '粉丝',
        following: '关注',
        noHistory: '暂无观看历史',
        noFavorites: '暂无收藏',
      },
      // 设置
      settings: {
        title: '设置',
        language: '语言',
        timezone: '时区',
        notifications: '通知',
        emailNotifications: '邮件通知',
        pushNotifications: '推送通知',
        saved: '设置已保存',
      },
      // 错误
      errors: {
        notFound: '页面未找到',
        serverError: '服务器错误',
        unauthorized: '未授权访问',
        forbidden: '禁止访问',
        networkError: '网络错误，请检查网络连接',
      },
      // 时间
      time: {
        justNow: '刚刚',
        minutesAgo: '{{count}}分钟前',
        hoursAgo: '{{count}}小时前',
        daysAgo: '{{count}}天前',
      },
    },
  },
};

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources,
    fallbackLng: 'en',
    debug: false,
    interpolation: {
      escapeValue: false, // React already escapes values
    },
    detection: {
      order: ['localStorage', 'navigator', 'htmlTag'],
      caches: ['localStorage'],
    },
  });

export default i18n;

// Supported languages
export const SUPPORTED_LANGUAGES = [
  { code: 'en', name: 'English', nativeName: 'English' },
  { code: 'zh', name: 'Chinese', nativeName: '中文' },
] as const;

// RTL languages
export const RTL_LANGUAGES = ['ar', 'he', 'fa', 'ur'];

// Check if language is RTL
export const isRTL = (lang: string): boolean => RTL_LANGUAGES.includes(lang);
