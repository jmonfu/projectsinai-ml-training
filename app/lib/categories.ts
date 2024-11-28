export const TASK_CATEGORIES = {
  'bug_fix': { name: 'Bug Fix', color: 'bg-red-100 text-red-800' },
  'feature': { name: 'Feature Request', color: 'bg-blue-100 text-blue-800' },
  'documentation': { name: 'Documentation', color: 'bg-green-100 text-green-800' },
  'enhancement': { name: 'Enhancement', color: 'bg-purple-100 text-purple-800' },
  'security': { name: 'Security', color: 'bg-orange-100 text-orange-800' },
  'performance': { name: 'Performance', color: 'bg-yellow-100 text-yellow-800' },
  'testing': { name: 'Testing', color: 'bg-indigo-100 text-indigo-800' },
  'ui_ux': { name: 'UI/UX', color: 'bg-pink-100 text-pink-800' },
  'devops': { name: 'DevOps', color: 'bg-cyan-100 text-cyan-800' },
  'development': { name: 'Development', color: 'bg-sky-100 text-sky-800' },
  'design': { name: 'Design', color: 'bg-violet-100 text-violet-800' },
  'research': { name: 'Research', color: 'bg-emerald-100 text-emerald-800' },
  'meeting': { name: 'Meeting', color: 'bg-amber-100 text-amber-800' },
  'planning': { name: 'Planning', color: 'bg-rose-100 text-rose-800' },
  'other': { name: 'Other', color: 'bg-gray-100 text-gray-800' }
} as const;

export type TaskCategory = keyof typeof TASK_CATEGORIES;

export const CATEGORY_LIST = Object.keys(TASK_CATEGORIES) as TaskCategory[]; 