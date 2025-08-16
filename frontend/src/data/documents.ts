import { computed, MaybeRefOrGetter, toValue } from 'vue'
import { useList } from 'frappe-ui/src/data-fetching'
import type { GPPage } from '@/types/doctypes'

// Temporary interface until types are auto-generated
interface GPExternalURL {
  name: string
  url: string
  title?: string
  service?: 'Figma' | 'Google Sheets' | ''
  project?: string
  pod?: string
  creation: string
  modified: string
}

export type DocumentItem = {
  name: string
  title: string
  type: 'page' | 'external_url'
  creation: string
  modified: string
  project?: string
  pod?: string
  // Page-specific fields
  content?: string
  slug?: string
  team?: string
  // External URL-specific fields
  url?: string
  service?: string
}

interface UseDocumentsOptions {
  filters: {
    project?: string
    pod?: string
  }
  orderBy?: 'title asc' | 'modified desc' | 'creation desc'
}

export function useDocuments(options: UseDocumentsOptions) {
  const { filters, orderBy = 'modified desc' } = options

  // Fetch pages
  const pages = useList<
    Pick<
      GPPage,
      'name' | 'title' | 'content' | 'slug' | 'project' | 'team' | 'pod' | 'creation' | 'modified'
    >
  >({
    doctype: 'GP Page',
    fields: ['name', 'title', 'content', 'slug', 'project', 'team', 'pod', 'creation', 'modified'],
    filters: filters,
    orderBy: orderBy,
    cacheKey: ['Documents_Pages', filters, orderBy],
  })

  // Fetch external URLs
  const externalUrls = useList<GPExternalURL>({
    doctype: 'GP External URL',
    fields: ['name', 'url', 'title', 'service', 'project', 'pod', 'creation', 'modified'],
    filters: filters,
    orderBy: orderBy,
    cacheKey: ['Documents_ExternalURLs', filters, orderBy],
  })

  // Merge and sort documents
  const documents = computed(() => {
    const pageItems: DocumentItem[] = (pages.data || []).map((page) => ({
      name: page.name,
      title: page.title || 'Untitled',
      type: 'page' as const,
      creation: page.creation,
      modified: page.modified,
      project: page.project,
      pod: page.pod,
      content: page.content,
      slug: page.slug,
      team: page.team,
    }))

    const urlItems: DocumentItem[] = (externalUrls.data || []).map((url) => ({
      name: url.name,
      title: url.title || 'External Link',
      type: 'external_url' as const,
      creation: url.creation,
      modified: url.modified,
      project: url.project,
      pod: url.pod,
      url: url.url,
      service: url.service,
    }))

    const allItems = [...pageItems, ...urlItems]

    // Sort the merged items
    if (orderBy === 'title asc') {
      return allItems.sort((a, b) => a.title.localeCompare(b.title))
    } else if (orderBy === 'modified desc') {
      return allItems.sort(
        (a, b) => new Date(b.modified).getTime() - new Date(a.modified).getTime(),
      )
    } else if (orderBy === 'creation desc') {
      return allItems.sort(
        (a, b) => new Date(b.creation).getTime() - new Date(a.creation).getTime(),
      )
    }

    return allItems
  })

  const isLoading = computed(() => pages.loading || externalUrls.loading)
  const error = computed(() => pages.error || externalUrls.error)

  return {
    documents,
    isLoading,
    error,
    // Expose individual lists for operations
    pages,
    externalUrls,
    reload: () => {
      pages.reload()
      externalUrls.reload()
    },
  }
}
