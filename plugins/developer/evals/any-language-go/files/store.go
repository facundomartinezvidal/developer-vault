package store

type Store struct {
	data map[string]string
}

func New() *Store {
	return &Store{data: map[string]string{}}
}

func (s *Store) Set(k, v string) {
	s.data[k] = v
}

func (s *Store) Get(k string) string {
	return s.data[k]
}
