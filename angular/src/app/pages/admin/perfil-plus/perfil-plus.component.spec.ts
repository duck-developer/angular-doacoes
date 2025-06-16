import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PerfilPlusComponent } from './perfil-plus.component';

describe('PerfilPlusComponent', () => {
  let component: PerfilPlusComponent;
  let fixture: ComponentFixture<PerfilPlusComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PerfilPlusComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PerfilPlusComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
