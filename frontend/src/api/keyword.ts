import request from '@/utils/request'

export type KeywordCategory = 'company' | 'product' | 'domain' | 'ip'

export interface Keyword {
  id?: number
  word: string
  category: KeywordCategory
  description?: string
  is_active?: boolean
  match_count?: number
  last_match_time?: string
}

export interface KeywordResponse {
  code: number
  message: string
  data: {
    items: Keyword[]
    total: number
  }
}

export interface KeywordCreateResponse {
  code: number
  message: string
  data: {
    id: number
  }
}

export interface KeywordUpdateResponse {
  code: number
  message: string
}

export function getKeywords(params?: {
  page?: number
  page_size?: number
  word?: string
  category?: KeywordCategory
  is_active?: boolean
}) {
  return request<KeywordResponse>({
    url: '/v1/keywords',
    method: 'get',
    params
  })
}

export function createKeyword(data: Keyword) {
  return request<KeywordCreateResponse>({
    url: '/v1/keywords',
    method: 'post',
    data
  })
}

export function updateKeyword(id: number, data: Keyword) {
  return request<KeywordUpdateResponse>({
    url: `/v1/keywords/${id}`,
    method: 'put',
    data
  })
}

export function deleteKeyword(id: number) {
  return request<KeywordUpdateResponse>({
    url: `/v1/keywords/${id}`,
    method: 'delete'
  })
} 